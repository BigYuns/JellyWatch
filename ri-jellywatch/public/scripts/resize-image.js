var maxImageDimension = 1000;
resizeImageFileForUpload = function(file, callback) {
  var img = document.createElement("img");
  img.onload = function() {
	URL.revokeObjectURL(img.src);
	var scale = Math.min(1, Math.min(maxImageDimension / img.width, maxImageDimension / img.height));
    var canvas = document.createElement("canvas");
    var ctx = canvas.getContext("2d");
    canvas.width = img.width * scale;
    canvas.height = img.height * scale;
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    var url = canvas.toDataURL("image/jpeg");
	callback(url);
  };
  img.src = URL.createObjectURL(file);
}
