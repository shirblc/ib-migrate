from flask import Flask, render_template, jsonify, abort
import os
import zipfile
from convert_to_wp import main


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = {'zip'}

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Routes
    # -----------------------------------------------------------------
    # Endpoint: GET /
    # Description: Returns the upload form.
    @app.route('/')
    def index():
        return render_template('upload.html')

    # Endpoint: POST /
    # Description: Upload the backup.
    @app.route('/', methods=['POST'])
    def upload_backup():
        uploaded_backup = request.form.get('fileUpload')
        file_extension = uploaded_backup.filename.rsplit('.', 1)[1].lower()

        # If the uploaded file is a ZIP file, unzip it and run the
        # script to convert it to a Wordpress XML.
        if file_extension in ALLOWED_EXTENSIONS:
            uploaded_backup.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                 uploaded_backup.filename))
            file_path = 'uploads/' + uploaded_backup.filename
            with zipfile.ZipFile(file_path) as file:
                file.extractall('./uploads')
            os.remove(file_path)
            main()
        # Otherwise abort
        else:
            abort(400)

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
