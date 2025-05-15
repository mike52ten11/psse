

// let yearCheckboxes = document.querySelectorAll('year');
// const 年份打勾 = document.querySelectorAll('.year')

document.addEventListener('DOMContentLoaded', function() {
    let yearCheckboxes = document.querySelectorAll('year');
    let additionalFields = document.getElementById('additionalFields');
    console.log('嗨');
    yearCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            checkOnlyOne(this);
            handleYearSelection();
        });
    });

    function checkOnlyOne(checkbox) {
        yearCheckboxes.forEach(item => {
            if (item !== checkbox) item.checked = false;
        });
    }

    function handleYearSelection() {
        const selectedYear = Array.from(yearCheckboxes).find(checkbox => checkbox.checked);
        
        if (selectedYear) {
            additionalFields.style.display = 'block';
            fetchBusList(selectedYear.value);
        } else {
            additionalFields.style.display = 'none';
        }
    }

    function fetchBusList(year) {
        fetch(`/api/bus-list/?year=${year}&user=${username}&labeltype=bus`)
            .then(response => response.json())
            .then(jsonResponse => {
                if (jsonResponse.data) {
                    populateBusDropdown(jsonResponse.data);
                } else {
                    console.error('API response does not contain data');
                }
            })
            .catch(error => {
                console.error('Error fetching bus list:', error);
            });
    }


}
);

// function checkOnlyOne(checkbox) 
// {
//     var checkboxes = document.getElementsByName('year')
//     checkboxes.forEach((item) => 
//                 {
//                     if (item !== checkbox) item.checked = false
//                 }
//             )
// }

// function toggleAdditionalFields(checkbox) {
//     var checkboxes = document.getElementsByName('year');
//     var additionalFields = document.getElementById('additionalFields');
//     var selectedYear = Array.from(checkboxes).find(checkbox => checkbox.checked);
//     if (selectedYear) 
//     {
//         additionalFields.style.display = 'block';
//         fetchBusList(selectedYear.value);
//     } 
//     else 
//     {
//         additionalFields.style.display = 'none';
//     }
// }
// function fetchBusList(year)
// {
//     var username = document.getElementById('hidden_username').value;
// // 假設你的 API 端點是 '/api/bus-list/'
//     fetch(`/api/bus-list/?year=${year}&user=${username}&labeltype=bus`)
//         .then(response => response.json())
//         .then(jsonResponse => {
//             if (jsonResponse.data) {
//                 populateBusDropdown(jsonResponse.data);
//             } else {
//                 console.error('API response does not contain data');
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching bus list:', error);
//         });
// }




// function populateBusDropdown(busList) 
// {
//     var select = document.getElementById('dynamic_bus');
//     select.innerHTML = ''; // 清空现有选项
    
//     busList.forEach(bus => {
//         var option = document.createElement('option');
//         option.value = bus.num;  // 使用 'num' 作为值
//         option.textContent = `${bus.num} - ${bus.name}`;  // 显示 'num' 和 'name'
//         select.appendChild(option);
//     });
// }
