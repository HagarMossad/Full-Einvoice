'use strict';
import App from './main.js'

const e = React.createElement;
const domContainer = document.querySelector('#App');
const root = ReactDOM.createRoot(domContainer);
root.render(e(App));