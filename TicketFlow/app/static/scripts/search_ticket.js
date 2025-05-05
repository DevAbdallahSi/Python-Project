const tableBody = document.getElementById('result');
    $(document).ready(function () {
    $('#search-input').on('input', function () {
      let query = $(this).val();
      let htmlString = '';
      $.ajax({
        url: "/search",
        data: {
          'q': query
        },
        success: function (data) {
          
          data.forEach(ticket => {
                    var status=''
                    if(ticket.status == 'Closed')  status=`<span class="badge bg-success">${ticket.status}</span>`
                    if(ticket.status == 'In progress')  status=`<span class="badge bg-warning text-dark">${ticket.status}</span>`
                    if(ticket.status == 'Open')  status=`<span class="badge bg-danger">${ticket.status}</span>`
                    else status=`<span class="badge bg-secondary">${ticket.status}</span>`
                    htmlString += `
                        <tr>
                    <td>${ticket.id}</td>
                    <td>${ticket.title}</td>
                    <td>${ticket.created_at}</td>
                    <td>${status}</td>
                    <td>${ticket.location}</td>
                    <td>${ticket.issuer}</td>
                    <td>${ticket.assigned_to}</td>
                    <td>
                      <a href="/ticket/${ticket.id}" class="btn btn-sm btn-info"><i class="bi bi-eye"></i></a>
                    </td>
                  </tr>
                    `;
                });
        },complete: function () {
            tableBody.innerHTML = htmlString;
        }
      });
    });
  });