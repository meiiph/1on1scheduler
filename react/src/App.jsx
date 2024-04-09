import { Component, Fragment } from "react";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import ContactsHome from "./Components/Contacts/ContactsHome";
import ViewEvents from "./Components/Event/ViewEvents";
import AddEvent from "./Components/Event/AddEvent"
import Auth from "./Components/Auth/Auth"
import NavBar from "./Components/Nav/Nav"
// import Calendar from "./Components/Calendar/Calendar";
// import React from "react";

class App extends Component {
  render () {
    return(
      <Fragment>
        <BrowserRouter>
          <NavBar/>
          <Routes>
            <Route path={'/'} element={<Auth/>}/>
            <Route path={'/contacts/'} element={<ContactsHome/>}/>
            {/* <Route path={'/calendars/'} element={<Calendar/>}/> */}
            <Route path={'/events/'} element={<ViewEvents/>}/>
            <Route path={'/add/'} element={<AddEvent/>}/>
          </Routes>
        </BrowserRouter>
      </Fragment>
    );
  }
}

export default App