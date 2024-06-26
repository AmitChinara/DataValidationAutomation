const form_container = document.getElementsByClassName('form-container');

const loadLoginPage = () => {
    fetch('http://localhost:12508/controller/loginpage')
        .then(response => {
            return response.json()
        })
        .then(data => {
            let value = data.logininfo;
            form_container[0].innerHTML = value;
        })
        .catch(error => form_container[0].innerHTML = `<marquee id = "marquee-text">UNABLE TO FETCH DATA FROM SERVER</marquee>`);
}

// loadLoginPage();