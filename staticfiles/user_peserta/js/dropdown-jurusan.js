const jurusan = ["jurusan-fk", "jurusan-fkg", "jurusan-fkm", "jurusan-ff", "jurusan-fik", "jurusan-fmipa", "jurusan-fasilkom", "jurusan-ft", "jurusan-fh", "jurusan-fpsiko", "jurusan-fisip", "jurusan-fib", "jurusan-feb", "jurusan-fia", "jurusan-vokasi"];
const dictJurusan = {'fk':'jurusan-fk', 'fkg':'jurusan-fkg', 'fkm':'jurusan-fkm', 'ff':'jurusan-ff', 'fik':'jurusan-fik','fmipa':'jurusan-fmipa','fasilkom':'jurusan-fasilkom','ft':'jurusan-ft','fh':'jurusan-fh','fpsiko':'jurusan-fpsiko','fisip':'jurusan-fisip','fib':'jurusan-fib','feb':'jurusan-feb','fia':'jurusan-fia','vokasi':'jurusan-vokasi',}

function showJurusan(s) {
    for (var i in dictJurusan) {
        var tag = document.getElementById(dictJurusan[i]);
        tag.style.display = 'none';
        document.getElementById("jurusan").style.display = 'none'
        document.getElementById("label-jurusan").style.display = 'none'

    }
    for (const key in dictJurusan) {
        if (s.value == key) {
            var tag = document.getElementById(dictJurusan[key]);
            tag.style.display = "block";
            document.getElementById("jurusan").style.display = 'block'
            document.getElementById("label-jurusan").style.display = 'block'
        }
    }
    console.log("yesus");
}