import React, { useState } from 'react';
import './Calendar.css';
import WeeklyCalendar from './WeeklyCalendar/WeeklyCalendar'

function Calendar() {
    const [view, setView] = useState('monthly'); // Default view is monthly

    const handleViewChange = (newView) => {
        setView(newView);
    };

    return (
        <div className="calendar">
            <div className="header">
                <button onClick={() => handleViewChange('weekly')}>Weekly View</button>
                <button onClick={() => handleViewChange('monthly')}>Monthly View</button>
                <button onClick={() => handleViewChange('daily')}>Daily View</button>
            </div>
            <div className="view">
                {/* Render calendar content based on the selected view */}
                {view === 'weekly' && <WeeklyCalendar/>}
                {view === 'monthly' && <p>Monthly Calendar</p>}
                {view === 'daily' && <p>Daily Calendar</p>}
            </div>
        </div>
    );
}


export default Calendar;
