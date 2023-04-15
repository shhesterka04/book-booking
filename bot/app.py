from flask import Flask, send_file
import pandas as pd
import tempfile
import database

app = Flask(__name__)
db = database.DatabaseConnector()

@app.route('/download/<int:book_id>')
def download_book_stats(book_id):
    #usage_data = db.get_book_usage(book_id)
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".xlsx", delete=False) as temp_file:
        df = pd.DataFrame(usage_data)
        if 'user_id' in df.columns:
            df = df.drop(columns=['user_id'])
        df.to_excel(temp_file, index=False)

        temp_file.seek(0)
        return send_file(temp_file, as_attachment=True, attachment_filename=f"book_{book_id}_stats.xlsx", cache_timeout=0)

if __name__ == '__main__':
    app.run()
