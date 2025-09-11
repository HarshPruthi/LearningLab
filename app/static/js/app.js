const courseSel = document.getElementById('course');
const resultsDiv = document.getElementById('results');
const studentBtn = document.getElementById('studentInfoBtn');
const studentGroup = document.getElementById('studentInputGroup');
const studentInput = document.getElementById('studentNumber');

function renderResults(data) {
  if (data.error) {
    resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
    return;
  }
  const { columns = [], rows = [] } = data;
  if (!columns.length) {
    resultsDiv.innerHTML = `<div class="alert alert-info">No results.</div>`;
    return;
  }
  const thead = `<thead><tr>${columns.map(c => `<th>${c}</th>`).join('')}</tr></thead>`;
  const tbody = `<tbody>${rows.map(r => `<tr>${r.map(v => `<td>${v ?? ''}</td>`).join('')}</tr>`).join('')}</tbody>`;
  resultsDiv.innerHTML = `<div class="card"><div class="card-body p-0"><div class="table-responsive"><table class="table table-sm table-striped mb-0">${thead}${tbody}</table></div></div></div>`;
}

async function runQuery(action, studentNumber) {
  try {
    const payload = { course: courseSel.value, action };
    if (studentNumber !== undefined && studentNumber !== null && `${studentNumber}`.trim() !== '') {
      payload.studentNumber = `${studentNumber}`.trim();
    }
    const res = await axios.post('/query', payload);
    renderResults(res.data);
  } catch (err) {
    const msg = err?.response?.data?.error || err.message || 'Request failed';
    resultsDiv.innerHTML = `<div class="alert alert-danger">${msg}</div>`;
  }
}

function showStudentInput() {
  studentGroup.style.display = '';
  studentInput.focus();
}

function hideStudentInput() {
  studentGroup.style.display = 'none';
  studentInput.value = '';
}

document.querySelectorAll('button[data-action]').forEach(btn => {
  btn.addEventListener('click', () => {
    const action = btn.getAttribute('data-action');
    if (action === 'Student information') {
      showStudentInput();
    } else {
      hideStudentInput();
      runQuery(action);
    }
  });
});

studentInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const value = studentInput.value;
    if (!value.trim()) {
      resultsDiv.innerHTML = `<div class="alert alert-warning">Please enter a student number.</div>`;
      return;
    }
    runQuery('Student information', value);
  }
});