// Get the modal
var modal = $("#record-modal");

// Get the <span> element that closes the modal
var span_reg = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
function openModal() {
  modal.fadeIn();
}

// When the user clicks on <span> (x), close the modal
span_reg.onclick = function() {
  modal.fadeOut();
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.fadeOut();
  }
}
// End Modal -----------------------------

// -------------------------------------------------

function readURL(input) {
  if (input.files && input.files[0]) {
    var name = document.getElementById("file-sound").files[0]['name'];
    $('#dropzone').text(name);
    $('.drop-container').css('background-color','#32e0c4');
  }
}

function send_data() {
  // Loading retrieval
  $('#retrieval-loading').css('display','block');
  $('#retrieval-loading').css('overflow','hidden');
  $('#retrieval').fadeOut();
  $('.lyric_text').remove();

  var input = document.querySelector('input[type="file"]').files[0];

  if (input === undefined) {
    input = soundFile.getBlob();
  }

  var data = new FormData();
  data.append('file',input);
  fetch('/retrieval', {
    method: 'POST',
    body: data
  }).then(function (response){

      if (response.status !== 200) {
        console.log('Response status was not 200:' + $(response.status));
        return ;
      }
      response.json().then(function (data){
        retrieval = data['message'];

        title = retrieval['Title'];
        singer = retrieval['Singer'];
        Img = retrieval['Image'];
        link = retrieval['URL'];
        song = retrieval['Song'];
        lyrics = retrieval['Lyrics'];

        var audio1 = document.getElementById('audio1');
        var audio2 = document.getElementById('audio2');
        var audio3 = document.getElementById('audio3');
        var audio4 = document.getElementById('audio4');

        $('#rank1-title').text(title[0]);
        $('#rank1-singer').text(singer[0]);
        $('#rank1-link').attr('href',link[0]);
        $('#rank1-img').attr('src',Img[0]);
        $('#rank1-song').attr('src',song[0]);

        $('#rank2-title').text(title[1]);
        $('#rank2-singer').text(singer[1]);
        $('#rank2-link').attr('href',link[1]);
        $('#rank2-img').attr('src',Img[1]);
        $('#rank2-song').attr('src',song[1]);

        $('#rank3-title').text(title[2]);
        $('#rank3-singer').text(singer[2]);
        $('#rank3-link').attr('href',link[2]);
        $('#rank3-img').attr('src',Img[2]);
        // $('#rank3-song').attr('src',song[2]);

        $('#rank4-title').text(title[3]);
        $('#rank4-singer').text(singer[3]);
        $('#rank4-link').attr('href',link[3]);
        $('#rank4-img').attr('src',Img[3]);
        // $('#rank4-song').attr('src',song[3]);

        audio1.load();
        audio2.load();
        // audio3.load();
        // audio4.load();

        for (let i = 0; i < lyrics.length; i++) {
          $('<p class = lyric_text>'+ lyrics[i] +'</p>').appendTo('.lyrics');
        }

        $('#retrieval').fadeIn();
        $('#retrieval-loading').css('display','none');
        $('#retrieval-loading').css('overflow','visible ');
      });
  });

}

// Record VieSound
let mic, recorder, soundFile;

function setup() {
  noCanvas();
  // create an audio in
  mic = new p5.AudioIn();

  // users must manually enable their browser microphone for recording to work properly!
  mic.start();

  // create a sound recorder
  recorder = new p5.SoundRecorder();

  // connect the mic to the recorder
  recorder.setInput(mic);

  // create an empty sound file that we will use to playback the recording
  soundFile = new p5.SoundFile();
}

function start_record() {
  if (mic.enabled) {
    getAudioContext().resume();
    recorder.record(soundFile);
  }
}

function stop_record() {
  if (mic.enabled) {
    recorder.stop();
  }
}

function play_record() {
  if (mic.enabled) {
    soundFile.play();
  }
}

function save_record() {
  if (mic.enabled) {
    saveSound(soundFile, 'mySound.wav');
  }
}
