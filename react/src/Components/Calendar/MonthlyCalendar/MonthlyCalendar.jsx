import React from 'react';
import './MonthlyCalendar.css'; // Import CSS for styling

const MonthCalendar = () => {
  const currentDate = new Date();
  const currentMonth = currentDate.getMonth();
  const currentYear = currentDate.getFullYear();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const startDay = new Date(currentYear, currentMonth, 1).getDay();

  const daysArray = [];
  for (let i = 0; i < startDay; i++) {
    daysArray.push(<div key={`empty-${i}`} className="empty-day"></div>);
  }
  for (let i = 1; i <= daysInMonth; i++) {
    daysArray.push(<div key={`day-${i}`} className="day">{i}</div>);
  }

  return (
    <div className="month-calendar">
      <div className="header">{currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}</div>
      <div className="weekdays">
        <div className="weekday">Mon</div>
        <div className="weekday">Tue</div>
        <div className="weekday">Wed</div>
        <div className="weekday">Thu</div>
        <div className="weekday">Fri</div>
        <div className="weekday">Sat</div>
        <div className="weekday">Sun</div>
      </div>
      <div className="days">
        {daysArray}
      </div>
    </div>
  );
};

export default MonthCalendar;
