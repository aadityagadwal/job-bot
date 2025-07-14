    // Scraper Status Table
    async function updateScraperStatusTable() {
        const tbody = document.getElementById('scraperStatusTableBody');
        if (!tbody) return;
        tbody.innerHTML = '<tr><td class="px-4 py-2" colspan="4">Checking scraper status...</td></tr>';
        try {
            const resp = await fetch('/api/scraper-status');
            const status = await resp.json();
            let html = '';
            for (const s of status) {
                html += `<tr>
                    <td class="px-4 py-2 font-mono">${s.name}</td>
                    <td class="px-4 py-2">
                        <span class="inline-block px-2 py-1 rounded text-xs font-bold ${s.status ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}">${s.status ? 'OK' : 'FAIL'}</span>
                    </td>
                    <td class="px-4 py-2">${s.status ? (s.count || 0) : '-'}</td>
                    <td class="px-4 py-2 text-xs text-red-700">${s.status ? '' : (s.error || '')}</td>
                </tr>`;
            }
            tbody.innerHTML = html;
        } catch (e) {
            tbody.innerHTML = '<tr><td class="px-4 py-2 text-red-700" colspan="4">Status check failed</td></tr>';
        }
    }
    updateScraperStatusTable();
    setInterval(updateScraperStatusTable, 30000);

    // API Status Table
    const apiEndpoints = [
        { path: '/api/jobs', label: 'Get Jobs' },
        { path: '/api/find-jobs', label: 'Find Jobs' },
        { path: '/api/test-system', label: 'Test System' },
        { path: '/api/scrape-remoteok', label: 'Scrape RemoteOK' },
        { path: '/api/test-email', label: 'Test Email' },
        { path: '/api/status', label: 'API Status' },
    ];
    async function updateApiStatusTable() {
        const tbody = document.getElementById('apiStatusTableBody');
        if (!tbody) return;
        tbody.innerHTML = '<tr><td class="px-4 py-2" colspan="2">Checking API status...</td></tr>';
        try {
            const resp = await fetch('/api/status');
            const status = await resp.json();
            let html = '';
            for (const ep of apiEndpoints) {
                let key = ep.label.toLowerCase().replace(/ /g, '_');
                // Map keys to status dict
                if (key === 'get_jobs') key = 'jobs';
                if (key === 'find_jobs') key = 'find_jobs';
                if (key === 'test_system') key = 'test_system';
                if (key === 'scrape_remoteok') key = 'scrape_remoteok';
                if (key === 'test_email') key = 'email_configured';
                if (key === 'api_status') key = 'jobs'; // always up if jobs is up
                const val = status[key];
                html += `<tr>
                    <td class="px-4 py-2 font-mono">${ep.path} <span class="text-gray-400">(${ep.label})</span></td>
                    <td class="px-4 py-2">
                        <span class="inline-block px-2 py-1 rounded text-xs font-bold ${val ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}">${val ? 'OK' : 'FAIL'}</span>
                    </td>
                </tr>`;
            }
            tbody.innerHTML = html;
        } catch (e) {
            tbody.innerHTML = '<tr><td class="px-4 py-2 text-red-700" colspan="2">Status check failed</td></tr>';
        }
    }
    updateApiStatusTable();
    setInterval(updateApiStatusTable, 10000);

    // Test Email button
    document.getElementById('testEmailBtn').addEventListener('click', async () => {
        showModal('Sending test email...');
        const resp = await fetch('/api/test-email', {method: 'POST'});
        const data = await resp.json();
        showModal(data.message || 'Test email sent!');
    });
    // Scrape RemoteOK button
    document.getElementById('scrapeRemoteOKBtn').addEventListener('click', async () => {
        showModal('Scraping RemoteOK, please wait...');
        const resp = await fetch('/api/scrape-remoteok', {method: 'POST'});
        const data = await resp.json();
        let msg = data.message || 'RemoteOK scraping complete!';
        if (data.jobs && Array.isArray(data.jobs)) {
            msg += `<br><br><b>${data.jobs.length} jobs found:</b><br>`;
            msg += data.jobs.slice(0, 10).map(j => `<div style='text-align:left; margin:4px 0;'><b>${j.title}</b> @ ${j.company} <a href='${j.url}' target='_blank'>[link]</a></div>`).join('');
            if (data.jobs.length > 10) msg += `<div>...and ${data.jobs.length - 10} more.</div>`;
        }
        showModal(msg);
        await loadJobs();
    });
document.addEventListener('DOMContentLoaded', function () {
    let allJobs = [];
    let filteredJobs = [];
    let currentPage = 1;
    const pageSize = 20;

    function renderTable() {
        const tableBody = document.getElementById('jobsTableBody');
        tableBody.innerHTML = '';
        const start = (currentPage - 1) * pageSize;
        const end = start + pageSize;
        const jobsToShow = filteredJobs.slice(start, end);
        jobsToShow.forEach(job => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${job.title || ''}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${job.company || ''}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${job.location || ''}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        job.applied ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }">
                        ${job.applied ? 'Applied' : 'Found'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">${job.date_found || ''}</td>
            `;
            tableBody.appendChild(row);
        });
        updatePagination();
    }

    function updatePagination() {
        const pageInfo = document.getElementById('pageInfo');
        const totalPages = Math.ceil(filteredJobs.length / pageSize) || 1;
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
        document.getElementById('prevPage').disabled = currentPage === 1;
        document.getElementById('nextPage').disabled = currentPage === totalPages;
    }

    document.getElementById('prevPage').addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });
    document.getElementById('nextPage').addEventListener('click', function () {
        const totalPages = Math.ceil(filteredJobs.length / pageSize) || 1;
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    });
    document.getElementById('searchInput').addEventListener('input', function (e) {
        const val = e.target.value.toLowerCase();
        filteredJobs = allJobs.filter(job =>
            (job.title || '').toLowerCase().includes(val) ||
            (job.company || '').toLowerCase().includes(val) ||
            (job.location || '').toLowerCase().includes(val)
        );
        currentPage = 1;
        renderTable();
    });
    document.getElementById('exportBtn').addEventListener('click', function () {
        let csv = 'Title,Company,Location,Status,Date\n';
        filteredJobs.forEach(job => {
            csv += `"${job.title || ''}","${job.company || ''}","${job.location || ''}","${job.applied ? 'Applied' : 'Found'}","${job.date_found || ''}"\n`;
        });
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'jobs_export.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    async function loadJobs() {
        const response = await fetch('/api/jobs');
        allJobs = (await response.json()).reverse();
        filteredJobs = allJobs;
        currentPage = 1;
        renderTable();
    }

    // Modal logic
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modalContent');
    const closeModal = document.getElementById('closeModal');
    function showModal(content) {
        modalContent.innerHTML = content;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    });

    // Test System button
    document.getElementById('testSystemBtn').addEventListener('click', async () => {
        showModal('Running system test...');
        const resp = await fetch('/api/test-system', {method: 'POST'});
        const data = await resp.json();
        showModal(`<b>System Test Output:</b><br><pre>${data.stdout || ''}</pre><br><b>Errors:</b><br><pre>${data.stderr || ''}</pre>`);
    });

    // Find Jobs button
    document.getElementById('findJobsBtn').addEventListener('click', async () => {
        showModal('Finding jobs, please wait...');
        const resp = await fetch('/api/find-jobs', {method: 'POST'});
        const data = await resp.json();
        if (data.jobs && data.jobs.length > 0) {
            let html = `<b>Latest Jobs:</b><ul style='margin-top:10px;'>`;
            data.jobs.forEach(job => {
                html += `<li><a href="${job.url}" target="_blank" class="text-blue-600 underline">${job.title} at ${job.company}</a> (${job.location})</li>`;
            });
            html += '</ul>';
            showModal(html);
        } else {
            showModal('No jobs found.');
        }
    });

    // Demo: scrape RemoteOK and show jobs in modal (optional, can be removed)
    // Uncomment to add a button for this feature
    // document.getElementById('remoteOkBtn').addEventListener('click', async () => {
    //     showModal('Scraping RemoteOK...');
    //     const resp = await fetch('/api/scrape-remoteok');
    //     const jobs = await resp.json();
    //     let html = `<b>RemoteOK Jobs:</b><ul style='margin-top:10px;'>`;
    //     jobs.forEach(job => {
    //         html += `<li><a href="${job.url}" target="_blank" class="text-blue-600 underline">${job.title} at ${job.company}</a> (${job.location})</li>`;
    //     });
    //     html += '</ul>';
    //     showModal(html);
    // });

    loadJobs();
    setInterval(loadJobs, 5 * 60 * 1000);
});