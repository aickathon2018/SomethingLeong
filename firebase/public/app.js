var choosedStyle;

$(function(){
	$("#main").hide();
	
	
});
document.addEventListener("DOMContentLoaded", event =>{
	const app = firebase.app();
	//console.log(app);
	const db = firebase.firestore();
	db.settings({
		timestampsInSnapshots: true
	});
	
	
	
	
var docRef = db.collection("users").doc("5hXIFzjhXy42bR3iAsKh");

docRef.get().then(function(doc) {
    if (doc.exists) {
        console.log("Document data:", doc.data());
    } else {
        // doc.data() will be undefined in this case
        console.log("No such document!");
    }
}).catch(function(error) {
    console.log("Error getting document:", error);
});




  // Get a reference to the database service

	

});

function googleLogin(){
	const provider = new firebase.auth.GoogleAuthProvider();
	firebase.auth().signInWithPopup(provider)
		.then(result => {
			const user = result.user;
			$("#username").html('Hello '+user.displayName);
			$("#loginpage").hide();
			$("#main").show(500);
			console.log(user) 
		}) 
		.catch(console.log)
}
function googleLogout(){
	firebase.auth().signOut()
		.then(
		function() {
			console.log('Signout Succesfull')
			$("#main").hide();
			$("#loginpage").show(500);
		}, function(error) {
			console.log('Signout Failed')  
	});
}


function updatePost(e){
	const db = firebase.firestore();
	const myPost = db.collection('posts').doc();
	
	myPost.create({
			foo: 'bar'
		}).then(res=>{
			console.log('Document written at'+res.updateTime);
		});
}



function upload(files){
	const storageRef=firebase.storage().ref();
	var i;
	for(i=0;i<files.length;i++){
		console.log(files[i]);
		var refer = storageRef.child(files[i].name);
		var task = refer.put(files[i])
		task.then(snapshot=>{
			console.log(snapshot)
			const url = snapshot.downloadURL
			
		})
	}
}
function uploadfiles(files){
	files.forEach(addStorage);
}
function addStorage(item){
	console.log(item);
	const storageRef=firebase.storage().ref();
	const refer = storageRef.child('${item.name}');
	const task = refer.put(item);
	task.then(snapshot=>{
		console.log(snapshot)
		const url = snapshot.downloadURL
		
	})
}

	const API_URL = 'https://face.recoqnitics.com/analyze'
	const ACCESS_KEY = '18f38db58e2375790160'
	const SECRET_KEY = 'f2c08046086c40ba811d5ff5fd46d26d9c0a4d78'
function uploadPhoto() {
	let formData = new FormData(document.forms.namedItem('fileinfo'))
	formData.append('access_key', ACCESS_KEY)
	formData.append('secret_key', SECRET_KEY)
	let xhr = new XMLHttpRequest()
	xhr.open('POST', API_URL)
	xhr.onload = () =>
    xhr.status === 200
      ? doSomethingWith(JSON.parse(xhr.response))
      : console.log(xhr.status)
	xhr.send(formData)
}

function doSomethingWith(data) {
  // do something with your data here
  console.log(data)
}

function selectStyle(){
	var e = document.getElementById("style");
	$("#imgholder").html("");
	//choosedStyle = e.selectedIndex;	
	choosedStyle = e.options[e.selectedIndex].value;
	console.log(choosedStyle)
	
	var storageRef = firebase.storage().ref();
	var database = firebase.database();
	var clothRef = database.ref('users/-LRXrmgXvbA-FdTZglQw/');
	clothRef.orderByChild("Style").equalTo(choosedStyle).on("child_added", function(data) {
   console.log(data.val().URL);
   
		
	var spaceRef = storageRef.child(data.val().URL);
	spaceRef.getDownloadURL().then(function(url) {
		$("#imgholder").append("<img src=\""+url+"\">");
		
		console.log(url);
		});
	
	});
	
	
}

function grabImg(){
	var storageRef = firebase.storage().ref();
	var spaceRef = storageRef.child('101845.jpg');
	spaceRef.getDownloadURL().then(function(url) {
		$("#my_image").attr("src",url);
		console.log(url);
	});
	
}
function show(){
	$("#my_image").attr("src","https://firebasestorage.googleapis.com/v0/b/aihackerthon.appspot.com/o/101845.jpg?alt=media&token=4b50ab5a-7dd7-4f97-88f7-81314ea17d52");
	
}
	