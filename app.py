import base64
import io

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Upload CSV data and display concentration plot."""
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if not uploaded_file:
            return render_template('index.html', error='No file provided')

        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            return render_template('index.html', error='Unable to read CSV file')

        if not {'time', 'concentration', 'dose'}.issubset(df.columns):
            return render_template(
                'index.html',
                error='CSV must contain time, concentration, and dose columns'
            )

        fig, ax = plt.subplots()
        ax.plot(df['time'], df['concentration'], marker='o')
        ax.set_xlabel('Time')
        ax.set_ylabel('Concentration')
        ax.set_title('Antibiotic Concentration Over Time')

        for t, d in zip(df['time'], df['dose']):
            ax.axvline(x=t, color='red', linestyle='--', alpha=0.3)
            ax.text(t, ax.get_ylim()[1], f'Dose: {d}', rotation=90, va='bottom', ha='center', fontsize=8)

        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        table_html = df.to_html(classes='table table-striped', index=False)
        return render_template('dashboard.html', plot_data=image_base64, table=table_html)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
