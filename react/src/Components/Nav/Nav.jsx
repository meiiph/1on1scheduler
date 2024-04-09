import { Fragment } from 'react';
import { Link } from 'react-router-dom';

let NavBar = () => {
    return (
        <Fragment>
            <nav className="navbar navbar-dark bg-dark navbar-expand-sm">
                <div className="container">
                    <Link to={'/home/'} className="navbar-brand">
                        <i className="fa fa-mobile text-warning"/>Home
                    </Link>
                    <Link to={'/contacts/'} className="navbar-brand">
                        <i className="fa fa-mobile text-warning"/>Contacts
                    </Link>
                    <Link to={'/invitations/'} className="navbar-brand">
                        <i className="fa fa-mobile text-warning"/>Invitations
                    </Link>
                    <Link to={'/calendars/'} className="navbar-brand">
                        <i className="fa fa-mobile text-warning"/>Calendars
                    </Link>
                </div>
            </nav>
        </Fragment>
    )
};

export default NavBar;