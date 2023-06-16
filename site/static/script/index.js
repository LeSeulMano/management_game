
$(document).ready(function () {
    if (document.URL == "http://127.0.0.1:8080/login") {

        // Auth

        $("#btn").on("click", function (e) {
            var sendInfo = {
                login: "test2",
                password: "slt"
            }
            $.post({
                url: "/login/auth",
                data: JSON.stringify({ login: "test2", password: "slt" }),
                contentType: "application/json",
                dataType: "text",
                success: function (data, textStatus) {
                    if (data) {
                        window.location.href = '/';
                    }
                }
            })
        })
    }
    else {


        $("#disconnect").on('click', function (e) {
            $.get("/logout").then(() => {
                location.reload()
            })
        })

        /// Loader ///

        setElement()
        loader()
        const id_user = parseInt(document.getElementById("village_id").innerText)
        var data = null;
        var seconds = 0;
        var minuts = 0;
        var hours = 0;
        $.get(`/village/${id_user}`).then((res) => {

            seconds = res.timer[0][0][4] + res.timer[0][0][5];
            minuts = res.timer[0][0][2] + res.timer[0][0][3]
            hours = res.timer[0][0][0] + res.timer[0][0][1]
            data = res
            document.getElementById('time_span').innerText = hours + ":" + minuts + ":" + seconds
        })

        $('[data-groupe="add-usine"]').on('click', function (e) {
            switch ($(this).parent().index()) {
                case 0:
                    $.get(`/addusine/Ferme`)
                        .done(function (data, textStatus, jqXHR) {
                            alert(data.message);
                            setElement()
                            loader()
                            setTimeout(function () {
                                $.get("finishusine/Ferme").then((res) => {
                                    alert("Construction fini !")
                                    setElement()
                                    loader()
                                })
                            }, data.message.slice(41, -7) * 1000)
                        })
                        .fail(function (jqXHR, textStatus, errorThrown) {
                            alert(jqXHR.responseJSON.message)
                        })
                    break;
                case 3:
                    $.get(`/addusine/Scierie`)
                        .done(function (data, textStatus, jqXHR) {
                            alert(data.message);
                            setElement()
                            loader()
                            setTimeout(function () {
                                $.get("finishusine/Scierie").then((res) => {
                                    alert("Construction fini !")

                                    setElement()
                                    loader()
                                })
                            }, data.message.slice(43, -7) * 1000)
                        })
                        .fail(function (jqXHR, textStatus, errorThrown) {
                            alert(jqXHR.responseJSON.message)
                        })
                    break;
                case 1:
                    $.get(`/addusine/Mine`)
                        .done(function (data, textStatus, jqXHR) {
                            alert(data.message);
                            setElement()
                            loader()
                            setTimeout(function () {
                                $.get("finishusine/Mine").then((res) => {
                                    alert("Construction fini !")

                                    setElement()
                                    loader()
                                })
                            }, data.message.slice(43, -7) * 1000)
                        })
                        .fail(function (jqXHR, textStatus, errorThrown) {
                            alert(jqXHR.responseJSON.message)
                        })
                    break;
                case 2:
                    $.get(`/addusine/Carrière`)
                        .done(function (data, textStatus, jqXHR) {
                            alert(data.message);
                            setElement()
                            loader()
                            setTimeout(function () {
                                $.get("finishusine/Carrière").then((res) => {
                                    alert("Construction fini !")

                                    setElement()
                                    loader()
                                })
                            }, data.message.slice(43, -7) * 1000)
                        })
                        .fail(function (jqXHR, textStatus, errorThrown) {
                            alert(jqXHR.responseJSON.message)
                        })
                    break;
                default:
                    break;
            }
            setElement()
        })
        $("#factory").on('click', function (e) {
            document.getElementsByClassName("choice-factory")[0].style.display = "flex"
            setElement()
        })
        $(".choice-factory").on('click', function (e) {
            if (e.target !== this) {
                return;
            }
            setElement()
            document.getElementsByClassName("choice-factory")[0].style.display = "none"
        })
        $("#close-choice-factory").on('click', function (e) {
            document.getElementsByClassName("choice-factory")[0].style.display = "none"
            setElement()
        })
        $(".level-entrepot").on('click', function (e) {
            $.get('levelup/True').done(function (data, textStatus, jqXHR) {
                alert(data.message);
                setElement()
                loader()
                setTimeout(function () {
                    $.get("levelup/False").then((res) => {
                        alert("Construction fini !")
                        setElement()
                        loader()
                    })
                }, data.message.slice(43, -7) * 1000)
            })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.responseJSON.message)
                })
        })
        $(".add-house").on('click', function (e) {
            $.get("addhouses/True").done(function (data, textStatus, jqXHR) {
                alert(data.message);
                setElement()
                loader()
                setTimeout(function () {
                    $.get("addhouses/False").then((res) => {
                        alert("Construction fini !")

                        setElement()
                        loader()
                    })
                }, data.message.slice(44, -7) * 1000)
            })
                .fail(function (jqXHR, textStatus, errorThrown) {
                    alert(jqXHR.responseJSON.message)
                })
        })
        $("#add-person").on('click', function (e) {
            document.getElementsByClassName("choice")[0].style.display = "flex"
            setElement()
        })
        $(".choice").on('click', function (e) {
            if (e.target !== this) {
                return;
            }
            setElement()
            document.getElementsByClassName("choice")[0].style.display = "none"
        })
        $("#close-choice").on('click', function (e) {
            document.getElementsByClassName("choice")[0].style.display = "none"
            setElement()
        })
        $('.adding_person').on('click', function (e) {
            $.get("/addpers").then((res) => {
                alert(res)
            })
            setElement()
        })
        $('[data-groupe="add"]').on('click', function (e) {
            switch ($(this).parent().index()) {
                case 0:
                    $.get(`/addwork/Ferme`).then((res) => {
                        alert(res)
                    })
                    break;
                case 1:
                    $.get(`/addwork/Scierie`).then((res) => {
                        alert(res)
                    })
                    break;
                case 2:
                    $.get(`/addwork/Mine`).then((res) => {
                        alert(res)
                    })
                    break;
                case 3:
                    $.get(`/addwork/Carrière`).then((res) => {
                        alert(res)
                    })
                    break;
                default:
                    break;
            }
            setElement()
        })
        $('[data-groupe="remove"]').on('click', function (e) {
            switch ($(this).parent().index()) {
                case 0:
                    $.get(`/removework/Ferme`).then((res) => {
                        alert(res)
                    })
                    break;
                case 1:
                    $.get(`/removework/Scierie`).then((res) => {
                        alert(res)
                    })
                    break;
                case 2:
                    $.get(`/removework/Mine`).then((res) => {
                        alert(res)
                    })
                    break;
                case 3:
                    $.get(`/removework/Carrière`).then((res) => {
                        alert(res)
                    })
                    break;
                default:
                    break;
            }
            setElement()
        })

        /// Timer ///


        setInterval(function () {
            if (minuts != 59) {
                minuts++
                $.get('/update_ressources/0')
            }
            else{
                minuts = 0;
                hours++
            }
            if (minuts%8 == 0){
                $.get('/update_ressources/1')
            }
            loader()
            document.getElementById('time_span').innerHTML = ((hours < 10 && hours.toString().length < 2) ? "0" + hours : hours) + ":" + ((minuts < 10 && minuts.toString().length < 2) ? "0" + minuts : minuts) + ":" + ((seconds < 10 && seconds.toString().length < 2) ? "0" + seconds : seconds)
        }, 60 * 1000);


        /// Set ///

    }



});



$(window).on("beforeunload", function () {
    var seconds = document.getElementById('time_span').innerHTML.slice(-2)
    var minuts = document.getElementById('time_span').innerHTML.slice(-5,-3)
    var hours = document.getElementById('time_span').innerHTML.slice(-8,-6)
    var time = hours + minuts + seconds
    $.post({
        url: "/leave",
        data: JSON.stringify({ time: time }),
        contentType: "application/json",
        dataType: "text",
    })
    return "leave"
});

function setElement() {
    const id_user = parseInt(document.getElementById("village_id").innerText)
    document.getElementsByClassName("wrapper")[0].innerHTML = ''
    document.getElementsByClassName("houses-container")[0].innerHTML = ''
    const housesHTML = `
    <div class="house-content">
        <div class="img"></div>
        <span>: 2</span>
    </div>
    `;

    const ferme = `<div class="factory">
    <div class="grange"></div>
    <div class="number">
        <div class="person"></div>
        <span class="number-factory">2/2</span>
    </div>
    </div>`
    $.get(`/village/${id_user}`).then((res) => {
        data = res
        document.getElementsByClassName("footer-hab")[0].innerHTML = "Nombre d'habitant qui travaille : " + (data['nbhabitant'][0][0] - data['working'][0][0]) + "/" + data['nbhabitant'][0][0]
        for (let i = 0; i < res.house.length; i++) {
            $(".houses-container").append(housesHTML)
            document.getElementsByClassName("house-content")[i].id = i
            document.getElementsByClassName("house-content")[i].children[1].innerHTML = ": " + res.house[i][1]
            if (res.house[i][1] == 0) {
                document.getElementsByClassName("house-content")[i].children[1].style.color = "red"
            }
        }
        document.getElementById("house-number").innerHTML = "x" + res.house.length
        document.getElementById("habitant-number").innerHTML = "x" + res.nbhabitant[0][0]
        for (let i = 0; i < res.factory.length; i++) {
            $(".wrapper").append(ferme)
            switch (res.factory[i][1]) {
                case "Ferme":
                    document.getElementsByClassName("grange")[i].style.backgroundImage = "url('/static/images/grange.png')"
                    break;
                case "Scierie":
                    document.getElementsByClassName("grange")[i].style.backgroundImage = "url('/static/images/scierie.png')"
                    break;
                case "Carrière":
                    document.getElementsByClassName("grange")[i].style.backgroundImage = "url('/static/images/stone.png')"
                    break;
                case "Mine":
                    document.getElementsByClassName("grange")[i].style.backgroundImage = "url('/static/images/mine.png')"
                    break;
                default:
                    break;
            }
            document.getElementsByClassName("number-factory")[i].innerHTML = ((res.factory[i][0] == null) ? 0 : res.factory[i][0]) + "/" + res.factory[i][2]
        }
    })
}
function loader() {
    const id_user = parseInt(document.getElementById("village_id").innerText)
    var tmp = 0
    $.get(`/village/${id_user}`).then((res) => {
        for (let i = 0; i < res.stock.length; i++) {
            switch (res.stock[i][0]) {
                case "Bois":
                    document.getElementsByClassName("food-quantity")[2].innerHTML = "x " + res.stock[i][1]
                    break;
                case "Pierre":
                    document.getElementsByClassName("food-quantity")[1].innerHTML = "x " + res.stock[i][1]
                    break;
                case "Nourriture":
                    document.getElementsByClassName("food-quantity")[0].innerHTML = "x " + res.stock[i][1]
                    break;
                case "Fer":
                    document.getElementsByClassName("food-quantity")[3].innerHTML = "x " + res.stock[i][1]
                    break;
                default:
                    break;
            }
            tmp = tmp + res.stock[i][1]
        }
        document.getElementsByClassName('total-res')[0].innerText = tmp.toFixed(1) + " /" + res.level_entre[0][1];
        document.getElementsByClassName("level-entre")[0].innerHTML = "Level : " + res.level_entre[0][0]

        if (document.getElementsByClassName("total-res")[0].innerHTML.slice(0, 3) == document.getElementsByClassName("total-res")[0].innerHTML.slice(5)) {
            document.getElementsByClassName("total-res")[0].style.color = "red"
        } else {
            document.getElementsByClassName("total-res")[0].style.color = "black"
        }
    })
}