// import Auth from "./Components/Auth/Auth"
// import Nav from "./Components/Nav/Nav"
// import Calendar from "./Components/Calendar/Calendar";
// import React from "react";
import ContactList from "./Components/Contacts/ContactList"
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {

  return(
    <BrowserRouter>
      <Routes>
        <Route path={'/'}/>
        <Route path={'/contacts/'} element={<ContactList/>}/>
      </Routes>
    </BrowserRouter>
  );

}

export default App