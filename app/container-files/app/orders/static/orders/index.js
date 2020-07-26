document.addEventListener('DOMContentLoaded', () => {

    if (document.querySelector("title").dataset.page === "menu"){

        // PIZZAS
        pizzas = document.querySelectorAll(".pizza");
        pizzas.forEach((pizzaButton) => {

            // Get name:
            let pizza = pizzaButton.value;
            
            // When "+" button is clicked, show all the selections:
            pizzaButton.addEventListener('click', () => {
                document.querySelector(`#pizza${pizza}added`).style.display = 'none';
                document.querySelector(`#pizza${pizza}plus`).style.display = 'none';
                document.querySelector(`#pizza${pizza}size`).style.display = 'block';
                document.querySelector(`#toppings${pizza}`).style.display = 'block';
                document.querySelector(`#pizza${pizza}quantity`).style.display = 'block';
                document.querySelector(`#pizza${pizza}price`).style.display = 'block';
                document.querySelector(`#pizza${pizza}buttons`).style.display = 'block';
                document.querySelector(`#pizza${pizza}`).style.borderBottom = "0.1rem solid lightGrey";

                let sizeSelector = document.querySelector(`#pizza${pizza}sizeSelect`);

                let quantSelector = document.querySelector(`#pizza${pizza}quantitySelect`);

                // Function to calculate price of selection
                updatePrice = (pizza) => {

                    // Size price
                    let sizePrice = 0;
                    if (sizeSelector.options[sizeSelector.selectedIndex].value === "Small") {
                        sizePrice = parseFloat(document.querySelector(`#pizza${pizza}small_price`).dataset.price);
                    }
                    else {
                        sizePrice = parseFloat(document.querySelector(`#pizza${pizza}large_price`).dataset.price);
                    }
                    document.querySelector(`#pizza${pizza}price`).setAttribute('data-unit_price', sizePrice);

                    // Get quantity
                    let quantity = 1;
                    quantity = quantSelector.options[quantSelector.selectedIndex].value;

                    // Display price
                    total = (sizePrice * quantity).toFixed(2);
                    document.querySelector(`#pizza${pizza}price`).innerHTML = `$${total}`;
                };

                updatePrice(pizza);

                // When another size or quantity is selected ---> change the price:
                sizeSelector.onchange = () => updatePrice(pizza);
                quantSelector.onchange = () => updatePrice(pizza);

                // Function for resetting pizza row
                hidePizza = (pizza) => {

                    // Hide pizza sections:
                    document.querySelector(`#pizza${pizza}size`).style.display = 'none';
                    document.querySelector(`#toppings${pizza}`).style.display = 'none';
                    document.querySelector(`#pizza${pizza}quantity`).style.display = 'none';
                    document.querySelector(`#pizza${pizza}price`).style.display = 'none';
                    document.querySelector(`#pizza${pizza}buttons`).style.display = 'none';
                    document.querySelector(`#pizza${pizza}msg`).style.display = 'none';

                    // Hide bottom line
                    document.querySelector(`#pizza${pizza}`).style.borderBottom = "0rem";

                    // Show "+" button
                    document.querySelector(`#pizza${pizza}plus`).style.display = 'block';

                    // Reset selected elements
                    for (var i = document.querySelector(`#pizza${pizza}`).getElementsByTagName('select').length - 1; i >= 0; --i) {
                        document.querySelector(`#pizza${pizza}`).getElementsByTagName('select')[i].selectedIndex = 0;
                    }

                };

                document.querySelector(`#pizza${pizza}add`).onclick = () => {

                    // Fetching name of every selected topping (if exists):
                    try {
                        let topping_1selector = document.querySelector(`#topping_1${pizza}select`);
                        var topping_1name = topping_1selector.options[topping_1selector.selectedIndex].dataset.name;
                    } catch (error) {
                        var topping_1name = "None 1";
                    }

                    try {
                        let topping_2selector = document.querySelector(`#topping_2${pizza}select`);
                        var topping_2name = topping_2selector.options[topping_2selector.selectedIndex].dataset.name;
                    } catch (error) {
                        var topping_2name = "None 2";
                    }

                    try {
                        let topping_3selector = document.querySelector(`#topping_3${pizza}select`);
                        var topping_3name = topping_3selector.options[topping_3selector.selectedIndex].dataset.name;
                    } catch (error) {
                        var topping_3name = "None 3";
                    }

                    try {
                        let topping_4selector = document.querySelector(`#topping_4${pizza}select`);
                        var topping_4name = topping_4selector.options[topping_4selector.selectedIndex].dataset.name;
                    } catch (error) {
                        var topping_4name = "None 4";
                    }

                    // If twice the same topping ---> display error msg
                    if (topping_1name === topping_2name || topping_1name === topping_3name || topping_1name === topping_4name || topping_2name === topping_3name || topping_2name === topping_4name || topping_3name === topping_4name) {
                        $(`#pizza${pizza}msg`).fadeIn(400).delay(4000).fadeOut(2000);
                    }

                    else {
                        // Send pizza data to the server through an Ajax request
                        $.ajax({
                            url:"pizza", 
                            type: "get",
                            data: {
                                pizza_id: pizza,
                                size: sizeSelector.options[sizeSelector.selectedIndex].value,
                                user: document.querySelector("#user").dataset.user,
                                quantity: quantSelector.options[quantSelector.selectedIndex].value,
                                topping_1: topping_1name,
                                topping_2: topping_2name,
                                topping_3: topping_3name,
                                topping_4: topping_4name
                            },
                            success: console.log("pizza sent to the server")
                        });

                        hidePizza(pizza);
                        $(`#pizza${pizza}added`).fadeIn(400).delay(700).fadeOut(2000);
                    }
                };

                // When cancel button clicked ---> hide sub sections
                document.querySelector(`#pizza${pizza}cancel`).onclick = () => hidePizza(pizza);

            });

        });

        // SUBS
        subs = document.querySelectorAll(".sub");
        subs.forEach((subButton) => {

            // Get name:
            let sub = subButton.value;

            // When "+" button is clicked, show all the selections:
            subButton.addEventListener('click', () => {
                document.querySelector(`#sub${sub}added`).style.display = 'none';
                document.querySelector(`#sub${sub}plus`).style.display = 'none';
                document.querySelector(`#sub${sub}size`).style.display = 'block';
                document.querySelector(`#extras${sub}`).style.display = 'block';
                document.querySelector(`#sub${sub}quantity`).style.display = 'block';
                document.querySelector(`#sub${sub}price`).style.display = 'block';
                document.querySelector(`#sub${sub}buttons`).style.display = 'block';
                document.querySelector(`#sub${sub}`).style.borderBottom = "0.1rem solid lightGrey";

                let sizeSelector = document.querySelector(`#sub${sub}sizeSelect`);

                let quantSelector = document.querySelector(`#sub${sub}quantitySelect`)

                // Function to calculate price of selection
                updatePrice = (sub) => {

                    // Size price
                    let sizePrice = 0;
                    let quantSelector = document.querySelector(`#sub${sub}quantitySelect`);
                    if (sizeSelector.options[sizeSelector.selectedIndex].value === "Small") {
                        sizePrice = parseFloat(document.querySelector(`#sub${sub}small_price`).dataset.price);
                    }
                    else {
                        sizePrice = parseFloat(document.querySelector(`#sub${sub}large_price`).dataset.price);
                    }
                    document.querySelector(`#sub${sub}price`).setAttribute('data-unit_price', sizePrice);

                    // Extra price
                    try {
                        let extra_1selector = document.querySelector(`#extra_1${sub}select`);
                        var extra_1price = parseFloat(extra_1selector.options[extra_1selector.selectedIndex].dataset.price);
                    } catch (error) {
                        var extra_1price = 0;
                    }

                    try {
                        let extra_2selector = document.querySelector(`#extra_2${sub}select`);
                        var extra_2price = parseFloat(extra_2selector.options[extra_2selector.selectedIndex].dataset.price);
                    } catch (error) {
                        var extra_2price = 0;
                    }

                    try {
                        let extra_3selector = document.querySelector(`#extra_3${sub}select`);
                        var extra_3price = parseFloat(extra_3selector.options[extra_3selector.selectedIndex].dataset.price);
                    } catch (error) {
                        var extra_3price = 0;
                    }

                    try {
                        let extra_4selector = document.querySelector(`#extra_4${sub}select`);
                        var extra_4price = parseFloat(extra_4selector.options[extra_4selector.selectedIndex].dataset.price);
                    } catch (error) {
                        var extra_4price = 0;
                    }

                    // Get quantity
                    let quantity = 1;
                    quantity = quantSelector.options[quantSelector.selectedIndex].value;

                    // Display price
                    total = ((sizePrice + extra_1price + extra_2price + extra_3price + extra_4price) * quantity).toFixed(2);
                    document.querySelector(`#sub${sub}price`).innerHTML = `$${total}`;
                };

                updatePrice(sub);

                // When another size or extra is selected ---> change the price:
                sizeSelector.onchange = () => updatePrice(sub);
                document.querySelector(`#extras${sub}`).onchange = () => updatePrice(sub);
                quantSelector.onchange = () => updatePrice(sub);

                // Function for resetting sub row
                hideSub = (sub) => {

                    // Hide sub sections
                    document.querySelector(`#sub${sub}size`).style.display = 'none';
                    document.querySelector(`#extras${sub}`).style.display = 'none';
                    document.querySelector(`#extras${sub}`).style.display = 'none';
                    document.querySelector(`#sub${sub}quantity`).style.display = 'none';
                    document.querySelector(`#sub${sub}price`).style.display = 'none';
                    document.querySelector(`#sub${sub}buttons`).style.display = 'none';
                    document.querySelector(`#sub${sub}msg`).style.display = 'none';

                    // Hide bottom line
                    document.querySelector(`#sub${sub}`).style.borderBottom = "0rem";

                    // Show "+" button
                    document.querySelector(`#sub${sub}plus`).style.display = 'block';

                    // Reset selected elements
                    for (var i = document.querySelector(`#sub${sub}`).getElementsByTagName('select').length - 1; i >= 0; --i) {
                        document.querySelector(`#sub${sub}`).getElementsByTagName('select')[i].selectedIndex = 0;
                    }
                };

                document.querySelector(`#sub${sub}add`).onclick = () => {

                    // Fetching name of every selected extra (if exists):
                    try {
                        let extra_1selector = document.querySelector(`#extra_1${sub}select`);
                        var extra_1name = extra_1selector.options[extra_1selector.selectedIndex].dataset.name;
                        if (extra_1name === "None") {
                            extra_1name = "None 1";
                        }
                    } catch (error) {
                        var extra_1name = "None 1";
                    }

                    try {
                        let extra_2selector = document.querySelector(`#extra_2${sub}select`);
                        var extra_2name = extra_2selector.options[extra_2selector.selectedIndex].dataset.name;
                        if (extra_2name === "None") {
                            extra_2name = "None 2";
                        }
                    } catch (error) {
                        var extra_2name = "None 2";
                    }

                    try {
                        let extra_3selector = document.querySelector(`#extra_3${sub}select`);
                        var extra_3name = extra_3selector.options[extra_3selector.selectedIndex].dataset.name;
                        if (extra_3name === "None") {
                            extra_3name = "None 3";
                        }
                    } catch (error) {
                        var extra_3name = "None 3";
                    }

                    try {
                        let extra_4selector = document.querySelector(`#extra_4${sub}select`);
                        var extra_4name = extra_4selector.options[extra_4selector.selectedIndex].dataset.name;
                        if (extra_4name === "None") {
                            extra_4name = "None 4";
                        }
                    } catch (error) {
                        var extra_4name = "None 4";
                    }

                    // If twice the same extra ---> display error msg
                    if (extra_1name === extra_2name || extra_1name === extra_3name || extra_1name === extra_4name || extra_2name === extra_3name || extra_2name === extra_4name || extra_3name === extra_4name) {
                        $(`#sub${sub}msg`).fadeIn(400).delay(4000).fadeOut(2000);
                    }

                    else {
                        // Send sub data to the server through an Ajax request
                        $.ajax({
                            url:"sub", 
                            type: "get",
                            data: {
                                name: document.querySelector(`#sub${sub}name`).dataset.name,
                                size: sizeSelector.options[sizeSelector.selectedIndex].value,
                                user: document.querySelector("#user").dataset.user,
                                quantity: quantSelector.options[quantSelector.selectedIndex].value,
                                extra_1: extra_1name,
                                extra_2: extra_2name,
                                extra_3: extra_3name,
                                extra_4: extra_4name
                            },
                            success: console.log("sub sent to the server")
                        });

                        hideSub(sub);
                        $(`#sub${sub}added`).fadeIn(400).delay(700).fadeOut(2000);
                    }
                };

                // When cancel button clicked ---> hide sub sections
                document.querySelector(`#sub${sub}cancel`).onclick = () => hideSub(sub);

            });

        });

        // PASTA
        pastas = document.querySelectorAll(".pasta");
        pastas.forEach((pastaButton) => {

            // Get name:
            let pasta = pastaButton.value;
            
            // When "+" button is clicked, show all the selections:
            pastaButton.addEventListener('click', () => {
                document.querySelector(`#pasta${pasta}added`).style.display = 'none';
                document.querySelector(`#pasta${pasta}plus`).style.display = 'none';
                document.querySelector(`#pasta${pasta}quantity`).style.display = 'block';
                document.querySelector(`#pasta${pasta}price`).style.display = 'block';
                document.querySelector(`#pasta${pasta}buttons`).style.display = 'block';
                document.querySelector(`#pasta${pasta}`).style.borderBottom = "0.1rem solid lightGrey";

                let quantSelector = document.querySelector(`#pasta${pasta}quantitySelect`);

                // Function to calculate price of selection
                updatePrice = (pasta) => {

                    // Get single price
                    let singlePrice = 0;
                    singlePrice = parseFloat(document.querySelector(`#pasta${pasta}singlePrice`).dataset.price);
                    document.querySelector(`#pasta${pasta}price`).setAttribute('data-unit_price', singlePrice);

                    // Get quantity
                    let quantity = 1;
                    quantity = quantSelector.options[quantSelector.selectedIndex].value;

                    // Display price
                    total = (singlePrice * quantity).toFixed(2);
                    document.querySelector(`#pasta${pasta}price`).innerHTML = `$${total}`;
                };

                updatePrice(pasta);

                // When another size or quantity is selected ---> change the price:
                quantSelector.onchange = () => updatePrice(pasta);

                // Function for resetting pasta row
                hidePasta = (pasta) => {

                    // Hide pasta sections:
                    document.querySelector(`#pasta${pasta}quantity`).style.display = 'none';
                    document.querySelector(`#pasta${pasta}price`).style.display = 'none';
                    document.querySelector(`#pasta${pasta}buttons`).style.display = 'none';

                    // Hide bottom line
                    document.querySelector(`#pasta${pasta}`).style.borderBottom = "0rem";

                    // Show "+" button
                    document.querySelector(`#pasta${pasta}plus`).style.display = 'block';

                };

                document.querySelector(`#pasta${pasta}add`).onclick = () => {

                    // Send pasta data to the server through an Ajax request
                    $.ajax({
                        url:"pasta",
                        type: "get",
                        data: {
                            name: document.querySelector(`#pasta${pasta}name`).dataset.name,
                            user: document.querySelector("#user").dataset.user,
                            quantity: quantSelector.options[quantSelector.selectedIndex].value,
                        },
                        success: console.log("pasta sent to the server")
                    });

                    hidePasta(pasta);
                    $(`#pasta${pasta}added`).fadeIn(400).delay(700).fadeOut(2000);
                };

                // When cancel button clicked ---> hide pasta sections
                document.querySelector(`#pasta${pasta}cancel`).onclick = () => hidePasta(pasta);

            });

        });

        // SALADS
        salads = document.querySelectorAll(".salad");
        salads.forEach((saladButton) => {

            // Get name:
            let salad = saladButton.value;
            
            // When "+" button is clicked, show all the selections:
            saladButton.addEventListener('click', () => {
                document.querySelector(`#salad${salad}added`).style.display = 'none';
                document.querySelector(`#salad${salad}plus`).style.display = 'none';
                document.querySelector(`#salad${salad}quantity`).style.display = 'block';
                document.querySelector(`#salad${salad}price`).style.display = 'block';
                document.querySelector(`#salad${salad}buttons`).style.display = 'block';
                document.querySelector(`#salad${salad}`).style.borderBottom = "0.1rem solid lightGrey";

                let quantSelector = document.querySelector(`#salad${salad}quantitySelect`);

                // Function to calculate price of selection
                updatePrice = (salad) => {

                    // Get single price
                    let singlePrice = 0;
                    singlePrice = parseFloat(document.querySelector(`#salad${salad}singlePrice`).dataset.price);
                    document.querySelector(`#salad${salad}price`).setAttribute('data-unit_price', singlePrice);

                    // Get quantity
                    let quantity = 1;
                    quantity = quantSelector.options[quantSelector.selectedIndex].value;

                    // Display price
                    total = (singlePrice * quantity).toFixed(2);
                    document.querySelector(`#salad${salad}price`).innerHTML = `$${total}`;
                };

                updatePrice(salad);

                // When another size or quantity is selected ---> change the price:
                quantSelector.onchange = () => updatePrice(salad);

                // Function for resetting salad row
                hideSalad = (salad) => {

                    // Hide salad sections:
                    document.querySelector(`#salad${salad}quantity`).style.display = 'none';
                    document.querySelector(`#salad${salad}price`).style.display = 'none';
                    document.querySelector(`#salad${salad}buttons`).style.display = 'none';

                    // Hide bottom line
                    document.querySelector(`#salad${salad}`).style.borderBottom = "0rem";

                    // Show "+" button
                    document.querySelector(`#salad${salad}plus`).style.display = 'block';

                };

                document.querySelector(`#salad${salad}add`).onclick = () => {

                    // Send salad data to the server through an Ajax request
                    $.ajax({
                        url:"salad",
                        type: "get",
                        data: {
                            name: document.querySelector(`#salad${salad}name`).dataset.name,
                            user: document.querySelector("#user").dataset.user,
                            quantity: quantSelector.options[quantSelector.selectedIndex].value,
                        },
                        success: console.log("salad sent to the server")
                    });

                    hideSalad(salad);
                    $(`#salad${salad}added`).fadeIn(400).delay(700).fadeOut(2000);
                };

                // When cancel button clicked ---> hide salad sections
                document.querySelector(`#salad${salad}cancel`).onclick = () => hideSalad(salad);

            });

        });

        // DINNER PLATTERS
        platters = document.querySelectorAll(".platter");
        platters.forEach((platterButton) => {

            // Get name:
            let platter = platterButton.value;
            
            // When "+" button is clicked, show all the selections:
            platterButton.addEventListener('click', () => {
                document.querySelector(`#platter${platter}added`).style.display = 'none';
                document.querySelector(`#platter${platter}plus`).style.display = 'none';
                document.querySelector(`#platter${platter}size`).style.display = 'block'
                document.querySelector(`#platter${platter}quantity`).style.display = 'block';
                document.querySelector(`#platter${platter}price`).style.display = 'block';
                document.querySelector(`#platter${platter}buttons`).style.display = 'block';
                document.querySelector(`#platter${platter}`).style.borderBottom = "0.1rem solid lightGrey";

                let sizeSelector = document.querySelector(`#platter${platter}sizeSelect`);

                let quantSelector = document.querySelector(`#platter${platter}quantitySelect`);

                // Function to calculate price of selection
                updatePrice = (platter) => {

                    // Size price
                    let sizePrice = 0;
                    if (sizeSelector.options[sizeSelector.selectedIndex].value === "Small") {
                        sizePrice = parseFloat(document.querySelector(`#platter${platter}small_price`).dataset.price);
                    }
                    else {
                        sizePrice = parseFloat(document.querySelector(`#platter${platter}large_price`).dataset.price);
                    }
                    document.querySelector(`#platter${platter}price`).setAttribute('data-unit_price', sizePrice);

                    // Get quantity
                    let quantity = 1;
                    quantity = quantSelector.options[quantSelector.selectedIndex].value;

                    // Display price
                    total = (sizePrice * quantity).toFixed(2);
                    document.querySelector(`#platter${platter}price`).innerHTML = `$${total}`;
                };

                updatePrice(platter);

                // When another size or quantity is selected ---> change the price:
                sizeSelector.onchange = () => updatePrice(platter);
                quantSelector.onchange = () => updatePrice(platter);


                // Function for resetting dinner platter row
                hidePlatter = (platter) => {

                    // Hide platter sections:
                    document.querySelector(`#platter${platter}size`).style.display = 'none';
                    document.querySelector(`#platter${platter}quantity`).style.display = 'none';
                    document.querySelector(`#platter${platter}price`).style.display = 'none';
                    document.querySelector(`#platter${platter}buttons`).style.display = 'none';

                    // Hide bottom line
                    document.querySelector(`#platter${platter}`).style.borderBottom = "0rem";

                    // Show "+" button
                    document.querySelector(`#platter${platter}plus`).style.display = 'block';

                    // Reset selected elements
                    for (var i = document.querySelector(`#platter${platter}`).getElementsByTagName('select').length - 1; i >= 0; --i) {
                        document.querySelector(`#platter${platter}`).getElementsByTagName('select')[i].selectedIndex = 0;
                    }

                };

                document.querySelector(`#platter${platter}add`).onclick = () => {

                    // Send dinner platter data to the server through an Ajax request
                    $.ajax({
                        url:"dinner_platter", 
                        type: "get",
                        data: {
                            name: document.querySelector(`#platter${platter}name`).dataset.name,
                            size: sizeSelector.options[sizeSelector.selectedIndex].value,
                            user: document.querySelector("#user").dataset.user,
                            quantity: quantSelector.options[quantSelector.selectedIndex].value
                        },
                        success: console.log("dinner platter sent to the server")
                    });

                    hidePlatter(platter);
                    $(`#platter${platter}added`).fadeIn(400).delay(700).fadeOut(2000);
                };

                // When cancel button clicked ---> hide dinner platters sections
                document.querySelector(`#platter${platter}cancel`).onclick = () => hidePlatter(platter);

            });

        });

    }

});
