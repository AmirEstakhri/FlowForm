document.addEventListener('DOMContentLoaded', function () {
    // Get the logged-in user's username from the hidden input or data attribute
    const loggedInUsername = document.getElementById('logged-in-username').dataset.username;
    console.log("Logged-in username:", loggedInUsername);

    // Clear any pre-selected options on page load for Managers and Users
    const managerSelect = document.getElementById('added_managers');
    const userSelect = document.getElementById('added_users');

    if (managerSelect) managerSelect.selectedIndex = -1; // Clear pre-selection
    if (userSelect) userSelect.selectedIndex = -1; // Clear pre-selection

    // Filter out the logged-in user's name from Managers and Users dropdowns
    if (managerSelect) {
        Array.from(managerSelect.options).forEach(option => {
            if (option.textContent.trim() === loggedInUsername) {
                option.remove();
            }
        });
    }

    if (userSelect) {
        Array.from(userSelect.options).forEach(option => {
            if (option.textContent.trim() === loggedInUsername) {
                option.remove();
            }
        });
    }

    // Manager Search
    const searchManagerBtn = document.getElementById('search_manager_btn');
    if (searchManagerBtn) {
        searchManagerBtn.addEventListener('click', function () {
            const searchQuery = document.getElementById('manager_search').value.toLowerCase();
            const managerOptions = document.querySelectorAll('#added_managers option');
            managerOptions.forEach(option => {
                const managerName = option.textContent.toLowerCase();
                option.style.display = managerName.includes(searchQuery) ? 'block' : 'none';
            });
        });
    }

    // User Search
    const searchUserBtn = document.getElementById('search_user_btn');
    if (searchUserBtn) {
        searchUserBtn.addEventListener('click', function () {
            const searchQuery = document.getElementById('user_search').value.toLowerCase();
            const userOptions = document.querySelectorAll('#added_users option');
            userOptions.forEach(option => {
                const userName = option.textContent.toLowerCase();
                option.style.display = userName.includes(searchQuery) ? 'block' : 'none';
            });
        });
    }

    // Add Manager to the assigned list
    document.getElementById('add_manager_btn').addEventListener('click', function () {
        const selectedManager = managerSelect.options[managerSelect.selectedIndex];
        if (!selectedManager) return; // No selection

        const managerId = selectedManager.value;
        const managerName = selectedManager.text;

        // Add manager to the assigned list
        const assignedManagerList = document.getElementById('assigned_managers_display');
        const listItem = document.createElement('li');
        listItem.innerHTML = `${managerName} <button class="remove-manager-btn" data-manager-id="${managerId}">Remove</button>`;
        assignedManagerList.appendChild(listItem);

        // Update receiver field
        const receiverField = document.getElementById('receiver');
        receiverField.value = receiverField.value ? `${receiverField.value}, ${managerName}` : managerName;

        // Remove from dropdown
        selectedManager.remove();

        // Add hidden input for form submission
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'assigned_managers';
        hiddenInput.value = managerId;
        document.querySelector('form').appendChild(hiddenInput);
    });

    // Add User to the assigned list
    document.getElementById('add_user_btn').addEventListener('click', function () {
        const selectedUser = userSelect.options[userSelect.selectedIndex];
        if (!selectedUser) return; // No selection

        const userId = selectedUser.value;
        const userName = selectedUser.text;

        // Add user to the assigned list
        const assignedUserList = document.getElementById('assigned_users_display');
        const listItem = document.createElement('li');
        listItem.innerHTML = `${userName} <button class="remove-user-btn" data-user-id="${userId}">Remove</button>`;
        assignedUserList.appendChild(listItem);

        // Update receiver field
        const receiverField = document.getElementById('receiver');
        receiverField.value = receiverField.value ? `${receiverField.value}, ${userName}` : userName;

        // Remove from dropdown
        selectedUser.remove();

        // Add hidden input for form submission
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'assigned_users';
        hiddenInput.value = userId;
        document.querySelector('form').appendChild(hiddenInput);
    });

    // Remove Manager from the assigned list
    document.getElementById('assigned_managers_display').addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-manager-btn')) {
            const managerId = event.target.getAttribute('data-manager-id');
            const managerName = event.target.parentElement.textContent.replace('Remove', '').trim();

            // Remove manager from the assigned list
            event.target.parentElement.remove();

            // Re-add to the dropdown
            const newOption = document.createElement('option');
            newOption.value = managerId;
            newOption.text = managerName;
            managerSelect.appendChild(newOption);

            // Remove hidden input for form submission
            const hiddenInput = document.querySelector(`input[name="assigned_managers"][value="${managerId}"]`);
            if (hiddenInput) hiddenInput.remove();

            // Update receiver field
            const receiverField = document.getElementById('receiver');
            receiverField.value = receiverField.value.replace(new RegExp(`,?\\s*${managerName}`), '').trim();
        }
    });

    // Remove User from the assigned list
    document.getElementById('assigned_users_display').addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-user-btn')) {
            const userId = event.target.getAttribute('data-user-id');
            const userName = event.target.parentElement.textContent.replace('Remove', '').trim();

            // Remove user from the assigned list
            event.target.parentElement.remove();

            // Re-add to the dropdown
            const newOption = document.createElement('option');
            newOption.value = userId;
            newOption.text = userName;
            userSelect.appendChild(newOption);

            // Remove hidden input for form submission
            const hiddenInput = document.querySelector(`input[name="assigned_users"][value="${userId}"]`);
            if (hiddenInput) hiddenInput.remove();

            // Update receiver field
            const receiverField = document.getElementById('receiver');
            receiverField.value = receiverField.value.replace(new RegExp(`,?\\s*${userName}`), '').trim();
        }
    });
});
