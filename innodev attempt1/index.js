const rf = document.getElementById("file");
const cbtn = document.getElementById("b2");
const ctxt = document.getElementById("b2txt");

cbtn.addEentListener("click", function() {
  rf.click();
});

rf.addEventListener("change", function() {
  if (rf.value) {
    ctxt.innerHTML = rf.value.match(
      /[\/\\]([\w\d\s\.\-\(\)]+)$/
    )[1];
  } else {
    ctxt.innerHTML = "No file chosen, yet.";
  }
});
