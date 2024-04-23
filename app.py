from flask import Flask, render_template, request
import os

app = Flask(__name__)

def detect_encoding(file_path):
    # List of encodings to try
    encodings = ['utf-8', 'utf-16']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1)  # Try reading one character to ensure the encoding is correct
            return encoding
        except UnicodeDecodeError:
            pass

    raise ValueError("Unable to detect encoding")

@app.route('/file_viewer/', defaults={'filename': 'file1.txt'})
@app.route('/file_viewer/<filename>', methods=['GET'])
def file_viewer(filename):
    try:
        # Check if the file exists
        file_path = os.path.join('files', filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        
        start_line = request.args.get('start_line', type=int)
        end_line = request.args.get('end_line', type=int)

        if start_line is not None and start_line <= 0:
            raise ValueError("Start line must be a positive integer greater than zero.")
        
        encoding = detect_encoding(file_path)
        
        with open(file_path, 'r', encoding=encoding) as file:
            lines = file.readlines()
            if end_line is not None and end_line > len(lines):
                raise ValueError("End line exceeds total number of lines in the file.")
            if start_line is not None and end_line is not None:
                lines = lines[start_line - 1:end_line]
            content = ''.join(lines)
        
        return render_template('file_viewer.html', content=content)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
