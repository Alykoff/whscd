<html>
<head>
<title>Index</title>
</head>
<body>
 <p>Cookie value</p>
 <textarea id="cookie"></textarea>
 <p>
    <button id="parse">Start</button>
 </p>
 <p>Result</p> 
 <textarea id="result"></textarea>
 <script>
  parse.onclick = () => {
    var cookie = document.getElementById('cookie').value;
    console.log(cookie);
    var xhr = new XMLHttpRequest();
    var base64Cookie = btoa(cookie);
    var params = 'cookie=' + encodeURIComponent(base64Cookie);
    xhr.open("GET", 'parse?' + params, true);
    xhr.onreadystatechange = (d) => {
     if (xhr.readyState != 4 || xhr.status != 200) {   
        return;
     }
     var resp = xhr.responseText; 
     var result = document.getElementById('result');
     result.value = resp;
    };
    xhr.send();
  };
 </script>
</body>
</html>
