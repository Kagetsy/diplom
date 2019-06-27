window.onload = function () {


	async function loginUser(login, password) {
		var response = await fetch(`login/${login}/${password}`);
		return await response.json();
	}

	var mybutton = document.getElementById('mybutton');
	mybutton.addEventListener('click', async function () {
		var login = document.getElementById('Inputlogin').value;
		var password = document.getElementById('InputPassword').value;
		var response = await loginUser(login, password);
		var loginForm = document.querySelector('#login');
		var navbar = document.querySelector('.navbar-js .container-fluid');
		loginForm.classList.add('hidden');
		navbar.innerHTML = (`<p class="navbar-text">${response.name}<p>
							<button type="button" class="btn btn-default navbar-btn">
							Выйти "::"
							</button>
							`);
	});
};