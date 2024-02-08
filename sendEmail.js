const nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: 'salomemahmoud@gmail.com',
        pass: 'lnvx qvqh sdlk sipl'
    }
});

let mailOptions = {
    from: 'salomemahmoud@gmail.com',
    to: 'salomemahmoud@gmail.com',
    subject: 'Meeting Invitation',
    text: 'You have been invited to a meeting from 3:30PM to 4:00 PM on 03/28/2024. Please log in to 1on1 Scheduler to accept or deny this invitation.'
};

transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
        console.error('Error occurred:', error);
    } else {
        console.log('Email sent:', info.response);
    }
});
