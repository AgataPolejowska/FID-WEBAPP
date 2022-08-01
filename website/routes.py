from deepface import DeepFace
from flask import jsonify, render_template, request, flash, redirect, url_for
from PIL import Image
import os

from website import app
from website.forms import IdentificationForm, RegisterForm, VerificationForm
from website.models import Person, FaceImage
from website.utils import MATCH_THRESHOLD, align_face, check_biometric_vector, check_one_face, check_valid_emotion, deepface_analyze, enhance_image_contrast, enhance_image_sharpness, get_biometrics_vector, get_key_points, perform_complex_preprocessing, prepare_img, resize_img
from website import db


TEMP_DIRECTORY = os.path.abspath('website/temp')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Starting page."""

    return render_template('main-page.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    """Registration module."""

    form = RegisterForm()

    if form.validate_on_submit:
        # If user entered nickname
        if  form.nickname.data != None:

            file = request.files['file']

            # If no file uploaded - redirect
            if file == None:
                return redirect(url_for('register'))

            # Get uploaded image path
            img_path = os.path.join(TEMP_DIRECTORY, file.filename)

            # Save uploaded image to website/temp project directory
            img = Image.open(file.stream)

            enhance_image_contrast(img, img_path, factor=1.2)
            enhance_image_sharpness(img, img_path, factor=2)

            # Check if one face on the image using MTCNN
            if (check_one_face(img_path) and check_valid_emotion(img_path)):

                perform_complex_preprocessing(img_path)
            
                # Generate and save image with face mesh
                # Get biometric vector
                biometric_vector = get_biometrics_vector(img_path)

                identified_list = check_biometric_vector(biometric_vector)

                # Add new person to database
                person = Person(
                    nickname=form.nickname.data,
                    w1=biometric_vector[0],
                    w2=biometric_vector[1],
                    w3=biometric_vector[2],
                    w4=biometric_vector[3],
                    w5=biometric_vector[4],
                    w6=biometric_vector[5],
                    w7=biometric_vector[6]
                )

                db.session.add(person)
                db.session.commit()

                flash("Registration performed successfully. The uploaded photo has met the requirements. The biometric vector based on the input face image has been generated.", 'success')
            #return redirect(url_for('register'))
            #os.remove(img_path)
    return render_template('registration-page.html', form=form)


@app.route('/verification', methods=['GET', 'POST'])
def verify():
    """Verification module."""
    form = VerificationForm()
    if request.method == 'POST':
        if  form.nickname.data != None:
            file = request.files['file']

            # If no file uploaded - redirect
            if file == None:
                return redirect(url_for('identify'))

            # Get uploaded image path
            img_path = os.path.join(TEMP_DIRECTORY, file.filename)

            # Save uploaded image to website/temp project directory
            img = Image.open(file.stream)
            
            enhance_image_contrast(img, img_path, factor=1.2)
            enhance_image_sharpness(img, img_path, factor=2)

            # Check if one face on the image using MTCNN
            if (check_one_face(img_path)):
                perform_complex_preprocessing(img_path)

                # Generate and save image with face mesh
                # Get biometric vector
                biometric_vector = get_biometrics_vector(img_path)

                identified_list = check_biometric_vector(biometric_vector)

                identified_flag = False

                for identified in identified_list:
                    if identified == form.nickname.data:
                        identified_flag = True
                        flash("Verified " + identified + " (found a similar biometric vector for the entered nickname according to the estimated acceptance threshold)", 'success')
                
                if not identified_flag:
                    flash('Verification failed. The system estimated that the entered nickname and the generated biometric vector do not match the saved reference vector or the vector does not exist yet in the currently available repository.', 'warning')

            os.remove(img_path)
    return render_template('verification-page.html', form=form)


@app.route('/identification', methods=['GET', 'POST'])
def identify():
    """Identification module."""

    form = IdentificationForm()

    if request.method == 'POST':
        file = request.files['file']

        # If no file uploaded - redirect
        if file == None:
            return redirect(url_for('identify'))

        # Get uploaded image path
        img_path = os.path.join(TEMP_DIRECTORY, file.filename)

        # Save uploaded image to website/temp project directory
        img = Image.open(file.stream)
        
        enhance_image_contrast(img, img_path, factor=1.2)
        enhance_image_sharpness(img, img_path, factor=2)

        # Check if one face on the image using MTCNN
        if (check_one_face(img_path)):
            perform_complex_preprocessing(img_path)

            # Generate and save image with face mesh
            # Get biometric vector
            biometric_vector = get_biometrics_vector(img_path)

            identified_list = check_biometric_vector(biometric_vector)

            for identified in identified_list:
                flash("Identified as " + identified + " (according to set threshold " + str(MATCH_THRESHOLD) + ")", 'success')

            if len(identified_list) == 0:
                flash("No similar individual biometric vector found in the current repository.", 'warning')
        os.remove(img_path)
    return render_template('identification-page.html', form=form)

@app.route('/requirements', methods=['GET', 'POST'])
def show_requirements():
    """Photo requirements page."""
    return render_template('requirements-page.html')

@app.route('/db-config')
def config_db():
    db.drop_all()
    db.create_all()
    test_user = Person(nickname='nickname_user_test', w1=1, w2=2, w3=3, w4=4, w5=5, w6=6, w7=7)
    test_upload = FaceImage(filename='filename_upload_test')
    db.session.add(test_user)
    db.session.add(test_upload)
    db.session.commit()
    db.session.delete(test_user)
    db.session.delete(test_upload)
    db.session.commit()
    return jsonify({'msg': 'Db restart'})

@app.route('/admin/autoregister', methods=['GET', 'POST'])
def autoregister():
    """The script for automatic biometric samples registration and saving to the database.
    """
    path_specified = ''
    for root, _, files in os.walk(path_specified, topdown=False):
        for name in files:
            img_path = os.path.join(root, name)

            img = Image.open(img_path)

            enhance_image_contrast(img, img_path, factor=1.2)
            enhance_image_sharpness(img, img_path, factor=2)

            # Check if one face on the image using MTCNN
            if (check_one_face(img_path)):

                perform_complex_preprocessing(img_path)

                # Generate and save image with face mesh
                # Get biometric vector
                biometric_vector = get_biometrics_vector(img_path)

                identified_list = check_biometric_vector(biometric_vector)
                print(identified_list)

                # Add new person to database
                person = Person(
                    nickname=os.path.splitext(name)[0],
                    w1=biometric_vector[0],
                    w2=biometric_vector[1],
                    w3=biometric_vector[2],
                    w4=biometric_vector[3],
                    w5=biometric_vector[4],
                    w6=biometric_vector[5],
                    w7=biometric_vector[6]
                )

                db.session.add(person)
                db.session.commit()
    return jsonify({'msg': 'registered'})
