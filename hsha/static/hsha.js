//hsha
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}



function logout()
{
    httpGet("logout")
}

function send_gamedata_validate()
{
	var words =  Array.from(document.querySelectorAll('input[name="checks"]')).map(x => x.value)
	var is_checked = new Array(words.length)
	is_checked = is_checked.fill(false)
	Array.from(document.querySelectorAll('input[name="checks"]:checked')).forEach(
		function(checked){
			is_checked[checked.id-1]=true
		});

	postData('/game/validate', { "words":words, "is_checked":is_checked })
  	.then(data => {
  		console.log(data);
    show_score(data);
    hide_game(); // JSON data parsed by `data.json()` call
  });

  	
  	
}

function hide_game(){
	var x = document.getElementById("game");
	x.style.display = "none";
}

function show_score(score) {
	var sv = document.getElementById("scorevalue")
	var s = document.getElementById("score")
	s.style.display = "block";
	sv.innerHTML = score;
}