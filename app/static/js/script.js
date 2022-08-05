function curex(selected){
  var currency = selected.value;
  document.getElementById("sum").innerHTML = contents["amounts"][currency];
}

function another(){
  document.getElementById("breakdown").innerHTML = "";
  document.getElementById("results").style.display = "none";
  document.getElementById("upload").style.display = "flex";
  document.getElementById("currency").options[0].selected = true;
  document.getElementById("processing").innerHTML = "processing";
}

//selecting all required elments
const dropArea = document.querySelector("#bounding-upload"),
dragText = dropArea.querySelector("#prompt"),
button = dropArea.querySelector("label"),
input = dropArea.querySelector("input"),
preview = document.getElementById("processed-image");

let file, sizeOfFile, nameOfFile, contents, base_url = "https://cocalc20.ai-camp.dev/b5c2a7f5-256b-4b99-ae4c-0f03a7aae105/port/8000/", reader=new FileReader(), intv;

input.addEventListener("change", function(){
    file = this.files[0];
    sizeOfFile = file.size;
    nameOfFile = file.name;
    dropArea.classList.add("used");
    uploadFile();
})

//if user drag file over box
dropArea.addEventListener("dragover", ()=>{
    event.preventDefault();
    // console.log("File is over DragArea");
    dropArea.classList.add("active");
    dragText.textContent = "release to upload image";
})

//if user leave drag file from box
dropArea.addEventListener("dragleave", ()=>{
    // console.log("File is outside DragArea");
    dropArea.classList.remove("active");
    dragText.textContent = "drag and drop an image";
})

//if user drop file into box
dropArea.addEventListener("drop", (event)=>{
    event.preventDefault();
    file = event.dataTransfer.files[0];
    sizeOfFile = file.size;
    nameOfFile = file.name;

    uploadFile();
});

function animToggle(start){
  clearInterval(intv);
  intv = false;
  processing = document.getElementById("processing");
  console.log("thing")

  if(start){
  console.log("started")
    intv = setInterval(function(){
  console.log("lioiop")
      let str = processing.innerHTML;
      if(str == "processing") processing.innerHTML = "processing.";
      else if(str == "processing.") processing.innerHTML = "processing..";
      else if(str == "processing..") processing.innerHTML = "processing...";
      else if(str == "processing...") processing.innerHTML = "processing";

      if(!intv){
        console.log("out?")
        clearInterval(intv);
      }
    }, 1000);
  }
}

async function uploadFile() {
    animToggle(true);
    reader.onloadend = function(){ preview.src = reader.result; }
    if(file)  reader.readAsDataURL(file);
    else preview.src = "";

    document.getElementById("upload").style.display = "none";
    document.getElementById("results").style.display = "flex";
    document.getElementById("processing").style.display = "flex";
    document.getElementById("new-image").style.display = "none";
    document.getElementById("info").style.display = "none";
    for(let xx of document.getElementsByClassName("drag-area")){
        xx.style.border = "1.5px solid var(--light)";
    }
    // document.getElementById("size-file").innerHTML = sizeOfFile.toString() + " bytes";
    // document.getElementById("name-file").innerHTML = nameOfFile.toString();
    dropArea.classList.remove("active");
    dropArea.classList.add("used");

    let formData = new FormData();
    formData.append("file", file);

    try {
        await fetch(base_url, {method: "POST", body: formData})
        .then(response => {
            // console.log(response);
            response.json().then(data => ({
              data: data,
              status: response.status
            })
          ).then(res => {
            contents = res.data
            console.log(contents);
            document.getElementById("processing").style.display = "none";
            document.getElementById("results").style.display = "flex";
            document.getElementById("info").style.display = "flex";
            document.getElementById("new-image").style.display = "flex";
            document.getElementById("sum").innerHTML = contents["amounts"]["USD"];
            animToggle();

            let breakdown = document.getElementById("breakdown");

            for(const [key, value] of Object.entries(contents["detections"])){
              console.log(value)
              let detection = document.createElement("p");
              detection.innerHTML = value + " x " + key + "<br>"
              detection.classList.add("secondary");
              breakdown.appendChild(detection)
            }
            imageAndClear();
          })
        });
     } catch(e) {
        console.log('Error while uploading data: ', e);
     }
}

async function setImage() {
  const promise = new Promise(resolve => resolve(42)); 
  preview.src = contents["result"];
  return "ok";
}
function imageAndClear(){
    setImage()
      .then(status => {
        console.log(status);
        fetch(base_url+"clear", {method: "GET"});
        console.log("done");
      })
      .catch(err => {
        console.log(err);
      });
}