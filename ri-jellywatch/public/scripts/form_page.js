$(function () {
    $(":file").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = imageIsLoaded;
            var url = reader.readAsDataURL(this.files[0]);
            console.log(url); 
            console.log(this.files[0]); 
            document.getElementById("myImg").style.display="block"
        }
    });
});

function imageIsLoaded(e) {
    $('#myImg').attr('src', e.target.result);
};