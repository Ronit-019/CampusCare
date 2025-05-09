CampusCare – Student Grievance Redressal System


CampusCare is a web-based grievance redressal platform developed using Flask. It enables students to raise academic or administrative issues which are tracked and managed by institution administrators. The system supports real-time escalation, email notifications, and a simple user dashboard.


---


 🚀 Features


- 🧑‍🎓 Student Registration & Login

- 🔐 Admin Dashboard with full grievance control

- 📝 Grievance Submission and Status Tracking

- ⏱️ Automatic Escalation of Unresolved Grievances (based on time)

- 📧 Email Notifications for Status Updates and Escalation

- 🔍 Role-based Access (Student/Admin)

- 🕒 Timezone-aware submission tracking using IST (Asia/Kolkata)


---


 🛠 Tech Stack


- Backend: Flask, SQLAlchemy

- Frontend: HTML, Jinja2 (via Flask Templates)

- Database: SQLite

- Email: Flask-Mail (Gmail SMTP)

- Others: Python `datetime`, `pytz`, and `dotenv` for config handling


---


 📁 Project Structure


```


CampusCare/

│

├── templates/

│   ├── index.html

│   ├── login.html

│   ├── register.html

│   ├── dashboard.html

│   ├── submit.html

│   ├── status.html

│   └── admin\_dashboard.html

│

├── static/

│   └── (optional CSS/JS files)

│

├── grievance.db               SQLite database file

├── app.py                     Main Flask application

├── .env                       Contains email credentials

└── README.md                  Project documentation


````


---


 ⚙️ Setup Instructions


 1. Clone the Repository


```bash

git clone https://github.com/Ronit-019/CampusCare.git

cd CampusCare

````


 2. Create and Activate Virtual Environment


```bash

python -m venv venv

source venv/bin/activate   On Windows: venv\Scripts\activate

```


 3. Setup Environment Variables


Create a `.env` file in the root directory:


```env

MAIL_USERNAME=your_email@gmail.com

MAIL_PASSWORD=your_app_password   Use App Password if using Gmail

```


 4. Run the Application


```bash

python app.py

```


Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.


---


 🔒 Admin Login (Default)


 Email: `admin@gmail.com`

 Password: `admin123`


---


 🔔 Email Configuration Notes


 Gmail SMTP is used.

 Ensure "Allow less secure apps" is turned ON or use an App Password if 2FA is enabled.

 Email is sent for:


   Grievance status updates

   Auto-escalation alerts


---


 🧪 Auto-Escalation Logic


Grievances that remain in "Pending" status for more than 1 minute (for demo purposes) are automatically escalated to "Escalated" and users are notified via email.


Modify the threshold in `auto_escalate()` for real-world usage.


---


 ✍️ Contributions


Feel free to fork the repository and submit pull requests! Open issues for bugs or new feature suggestions.


---


 📄 License


This project is open-source and available under the [MIT License](LICENSE).


---


 👨‍💻 Developed By


\Ronit Rajput – ICT Engineer, 3rd Year

Feel free to connect on https://www.linkedin.com/in/ronit-rajput-973602278 or reach out via email.



