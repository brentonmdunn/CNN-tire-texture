@app.route('/prediction/<file>')
def output(file):
    full_path = os.path.join(app.config['UPLOAD_DIRECTORY'], file)
    ouput = prediction(full_path)
    return render_template('output.html', type=ouput)
