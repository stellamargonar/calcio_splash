import * as React from "react";
import {Spinner} from "react-bootstrap";

export const Loader = () => {
    return (
        <Spinner animation="border" role="status" className="loader">
            <span className="visually-hidden">Caricamento...</span>
        </Spinner>
    );
}

