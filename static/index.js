// function setup() {
//   // The width and height of the captured photo. We will set the
//   // width to the value defined here, but the height will be
//   // calculated based on the aspect ratio of the input stream.

//   const width = 320; // We will scale the photo width to this
//   let height = 0; // This will be computed based on the input stream

//   // |streaming| indicates whether or not we're currently streaming
//   // video from the camera. Obviously, we start at false.

//   let streaming = false;

//   // The various HTML elements we need to configure or control. These
//   // will be set by the startup() function.

//   let video = null;
//   let canvas = null;
//   let photo = null;
//   let startbutton = null;

//   function showViewLiveResultButton() {
//     if (window.self !== window.top) {
//       // Ensure that if our document is in a frame, we get the user
//       // to first open it in its own tab or window. Otherwise, it
//       // won't be able to request permission for camera access.
//       document.querySelector(".contentarea").remove();
//       const button = document.createElement("button");
//       button.textContent = "View live result of the example code above";
//       document.body.append(button);
//       button.addEventListener("click", () => window.open(location.href));
//       return true;
//     }
//     return false;
//   }

//   function startup() {
//     if (showViewLiveResultButton()) {
//       return;
//     }
//     video = document.getElementById("video1");
//     canvas = document.getElementById("canvas");
//     photo = document.getElementById("photo");
//     startbutton = document.getElementById("startbutton");

//     navigator.mediaDevices
//       .getUserMedia({ video: true, audio: false })
//       .then((stream) => {
//         video.srcObject = stream;
//         video.play();
//       })
//       .catch((err) => {
//         console.error(`An error occurred: ${err}`);
//       });

//     video.addEventListener(
//       "canplay",
//       (ev) => {
//         if (!streaming) {
//           height = video.videoHeight / (video.videoWidth / width);

//           // Firefox currently has a bug where the height can't be read from
//           // the video, so we will make assumptions if this happens.

//           if (isNaN(height)) {
//             height = width / (4 / 3);
//           }

//           video.setAttribute("width", width);
//           video.setAttribute("height", height);
//           canvas.setAttribute("width", width);
//           canvas.setAttribute("height", height);
//           streaming = true;
//         }
//       },
//       false,
//     );

//     startbutton.addEventListener(
//       "click",
//       (ev) => {
//         takepicture();
//         ev.preventDefault();
//       },
//       false,
//     );

//     clearphoto();
//   }

//   // Fill the photo with an indication that none has been
//   // captured.

//   function clearphoto() {
//     const context = canvas.getContext("2d");
//     context.fillStyle = "#AAA";
//     context.fillRect(0, 0, canvas.width, canvas.height);

//     const data = canvas.toDataURL("image/jpeg", 1);
//     photo.setAttribute("src", data);
//   }

//   // Capture a photo by fetching the current contents of the video
//   // and drawing it into a canvas, then converting that to a PNG
//   // format data URL. By drawing it on an offscreen canvas and then
//   // drawing that to the screen, we can change its size and/or apply
//   // other changes before drawing it.

//   function takepicture() {
//     const context = canvas.getContext("2d");
//     if (width && height) {
//       canvas.width = width;
//       canvas.height = height;
//       context.drawImage(video, 0, 0, width, height);

//       const data = canvas.toDataURL("image/png");
//       photo.setAttribute("src", data);
//     } else {
//       clearphoto();
//     }
//   }

//   // Set up our event listener to run the startup process
//   // once loading is complete.
//   window.addEventListener("load", startup, false);

// }














(() => {

  const width = 320; // We will scale the photo width to this
  let height = 0; // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  let streaming = false;

  const videoElm = document.querySelector('#video');
  //const canvasElm = document.querySelector("#canvas");
  let canvasElm = null;
  const photoElm = document.getElementById("photo");

  const btnFront = document.querySelector('#btn-front');
  const btnBack = document.querySelector('#btn-back');
  const btnTakePhoto = document.querySelector("#btn-take-photo");

  let imgForm = document.getElementById("img_form");

  const supports = navigator.mediaDevices.getSupportedConstraints();
  if (!supports['facingMode']) {
    alert('Browser Not supported!');
    return;
  }

  let stream;

  const capture = async facingMode => {
    const options = {
      audio: false,
      video: {
        facingMode,
        zoom: true
      },
    };

    try {
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
      stream = await navigator.mediaDevices.getUserMedia(options);
    } catch (e) {
      alert(e);
      return;
    }
    videoElm.srcObject = null;
    videoElm.srcObject = stream;
    videoElm.play();
  }


  videoElm.addEventListener(
    "canplay",
    (ev) => {
      if (!streaming) {
        height = videoElm.videoHeight / (videoElm.videoWidth / width);

        if (isNaN(height)) {
          height = width / (4 / 3);
        }

        videoElm.setAttribute("width", width);
        videoElm.setAttribute("height", height);
        // canvasElm.setAttribute("width", width);
        // canvasElm.setAttribute("height", height);
        streaming = true;
      }
    },
    false,
  );

  btnBack.addEventListener('click', () => {
    capture('environment');
  });

  btnFront.addEventListener('click', () => {
    capture('user');
  });

  btnTakePhoto.addEventListener(
    "click",
    (ev) => {
      takePicture();
      ev.preventDefault();
    },
    false,
  );

  imgForm.onsubmit = (evt) => {
    console.log("onsubmit");
    console.log(photoElm.src.length);
    if (photoElm.src.length <= 10) {
        console.log("nothing to submit");
        evt.preventDefault();
        return false;
    } else {
        let imgContentElm = document.getElementById("img_content");
        imgContentElm.value = photoElm.src;
    }
    //evt.preventDefault();
  };

  let fileElm = document.getElementById("fileToUpload");

  fileElm.onchange = (evt) => {
        console.log('onchange');
        console.log(evt);
        let files = evt.target.files;
        // FileReader support
        if (FileReader && files && files.length) {
            var fr = new FileReader();
            fr.onload = function () {
                photoElm.src = fr.result;
                photoElm.width = width;
                console.log(`photoElm done.. width=${width}`);
            }
            fr.readAsDataURL(files[0]);
        }
        else {
            // fallback -- perhaps submit the input to an iframe and temporarily store
            // them on the server until the user's session ends.
            console.log("error: failed to load files : not supported");
        }
    };


  clearPhoto();


  function clearPhoto() {
    let canvasElm = document.createElement("canvas");
    canvasElm.setAttribute("id", "canvas");
    canvasElm.setAttribute("width", width);
    canvasElm.setAttribute("height", height);
    const context = canvasElm.getContext("2d");
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvasElm.width, canvasElm.height);

    const data = canvasElm.toDataURL("image/jpeg", 1);
    photoElm.setAttribute("src", data);
  }

  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  function takePicture() {
    let canvasElm = document.createElement("canvas");
    canvasElm.setAttribute("id", "canvas");
    canvasElm.setAttribute("width", width);
    canvasElm.setAttribute("height", height);
    const context = canvasElm.getContext("2d");
    if (width && height) {
      console.log("takePicture");
      canvasElm.width = width;
      canvasElm.height = height;
      context.drawImage(videoElm, 0, 0, width, height);

      const data = canvasElm.toDataURL("image/jpg", 1);
      photoElm.setAttribute("src", data);
      console.log("taken");
    } else {
      clearPhoto();
    }
  }

  console.log("init done..");
})();
