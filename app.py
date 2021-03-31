from flask import (
                   Flask,
                   render_template,
                   jsonify,
                   abort,
                   request,
                   redirect,
                   url_for,
                   send_file
                  )
import os
import zipfile
import random
import shutil
from pathlib import Path
from threading import Timer
from convert_to_wp import main


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = {'zip'}

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Routes
    # -----------------------------------------------------------------
    # Endpoint: GET /
    # Description: Returns the upload form.
    # Template rendering
    @app.route('/')
    def index():
        return render_template('upload.html')

    # Endpoint: POST /
    # Description: Upload the backup.
    # Uploading the file and redirecting
    @app.route('/', methods=['POST'])
    def upload_backup():
        uploaded_backup = request.files['fileUpload']
        file_extension = uploaded_backup.filename.rsplit('.', 1)[1].lower()
        directory = str(random.randint(1000000,9999999))

        # If the uploaded file is a ZIP file, unzip it and run the
        # script to convert it to a Wordpress XML.
        if file_extension in ALLOWED_EXTENSIONS:
            uploaded_backup.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                 uploaded_backup.filename))
            file_path = 'uploads/' + uploaded_backup.filename
            with zipfile.ZipFile(file_path) as file:
                directory_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                              directory)
                Path(directory_path).mkdir(parents=True)
                file.extractall(directory_path)
            os.remove(file_path)
            main(directory_path)
        # Otherwise abort
        else:
            abort(400)

        return redirect(url_for('download_form', backup_dir=directory))

    # Endpoint: GET /download
    # Description: Download the XML.
    # Template rendering
    @app.route('/download/<backup_dir>', methods=['GET'])
    def download_form(backup_dir):
        return render_template('download.html', backup_dir=backup_dir)

    # Endpoint: GET /download-file
    # Description: Download the XML.
    # Sending the download file
    @app.route('/download-file/<backup_dir>', methods=['GET'])
    def download_file(backup_dir):
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], backup_dir,
                                      'blog.xml'))

    # Endpoint: DELETE /backup/<backup_dir>
    # Description: Delete the backup data and the generated XML.
    # Deleting the backup files
    @app.route('/backup/<backup_dir>', methods=['DELETE'])
    def delete_folder(backup_dir):
        directory_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                      backup_dir)

        # Delete the relevant folder
        def remove_folder():
            shutil.rmtree(directory_path)

        # Start the timer to delete the folder after 10 minutes
        timer = Timer(600.0, remove_folder)
        timer.start()

        return jsonify({
            'success': True
        })

    # Error Handlers
    # -----------------------------------------------------------------
    # Bad request error handler
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'code': 400,
            'message': 'Bad request. Fix your request and try again.'
        }), 400

    # Not found error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'The resource you were looking for wasn\'t found.'
        }), 404

    # Method not allowed handler
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'code': 405,
            'message': 'This HTTP method is not allowed at this endpoint.'
        }), 405

    # Unprocessable error handler
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable request.'
        }), 422

    # Internal server error handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'An internal server error occurred.'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
