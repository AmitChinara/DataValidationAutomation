let login_info = `<div class="login-container data-container">
                <div class="login-inner-container">
                    <div class="input-title-container input-container">
                        <span id="login-text">Login</span>
                    </div>
                    <div class="input-username-container input-container">
                        <input type="text" class="input-design" id="username" placeholder="USERNAME">
                    </div>
                    <div class="input-password-container input-container">
                        <input type="password" class="input-design" id="password" placeholder="PASSWORD">
                    </div>
                    <div class="input-account-container input-container">
                        <span>ENVIRONMENT: </span>
                        <select id="account" class="input-design">
                            <option value="1">NON-PROD</option>
                            <option value="2">PRE-PROD</option>
                            <option value="3">PROD</option>
                        </select>
                    </div>
                    <div class="input-button-container input-container">
                        <div class="submit-button-container">
                            <input type="submit" class="input-design submit-button">
                        </div>
                    </div>
                </div>
            </div>`;


module.exports = {
    login_info
}