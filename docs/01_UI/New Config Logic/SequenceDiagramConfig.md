### 1. New Config Create (Создание новой конфигурации)
```mermaid
sequenceDiagram
    actor User
    participant Main
    participant ConfigLibrary
    participant ConfigEditorDialog
    participant DataBase@{ "type" : "database" }
    participant LocalData@{ "type" : "database" }

    User->>Main: Open Library
    Main->>ConfigLibrary: Open window
    User->>ConfigLibrary: Click "New Config"
    ConfigLibrary->>ConfigEditorDialog: Open empty dialog
    User->>ConfigEditorDialog: Input data
    User->>ConfigEditorDialog: Click "Save"
    ConfigEditorDialog->>DataBase: Save record
    ConfigEditorDialog->>LocalData: Set as active/last
    ConfigEditorDialog->>ConfigLibrary: Close & Refresh list
    ConfigLibrary->>Main: Change config & Return
```


### 2. Change Config (Изменение/Выбор активного конфига)
```mermaid
sequenceDiagram
    actor User
    participant Main
    participant ConfigLibrary
    participant LocalData@{ "type" : "database" }

    User->>Main: Open Library
    Main->>ConfigLibrary: Open window
    User->>ConfigLibrary: Select existing config
    User->>ConfigLibrary: Click "Change"
    ConfigLibrary->>LocalData: Update active config
    ConfigLibrary->>Main: Close & Return
```

### 3. Edit Config (Редактирование существующей конфигурации)
```mermaid
sequenceDiagram
    actor User
    participant ConfigLibrary
    participant ConfigEditorDialog
    participant DataBase@{ "type" : "database" }

    User->>ConfigLibrary: Select config
    User->>ConfigLibrary: Click "Edit"
    ConfigLibrary->>DataBase: Request data
    DataBase-->>ConfigLibrary: Return JSON/Object
    ConfigLibrary->>ConfigEditorDialog: Open with data (set sliders)
    User->>ConfigEditorDialog: Change values
    User->>ConfigEditorDialog: Click "Save"
    ConfigEditorDialog->>DataBase: Update record
    ConfigEditorDialog->>ConfigLibrary: Close & Refresh
```

### 4. Import Config (Импорт конфигурации)
```mermaid
sequenceDiagram
    actor User
    participant ConfigLibrary
    participant OS as System Dialog
    participant Validator
    participant DataBase@{ "type" : "database" }

    User->>ConfigLibrary: Click "Import"
    ConfigLibrary->>OS: Open file picker
    OS-->>ConfigLibrary: File content
    ConfigLibrary->>Validator: Validate (format check)
    alt is valid
        Validator-->>ConfigLibrary: OK
        ConfigLibrary->>DataBase: Save config
        ConfigLibrary->>ConfigLibrary: Update UI list
    else is invalid
        Validator-->>ConfigLibrary: Error
        ConfigLibrary->>User: Show error window
    end
```

### 5. Export Config (Экспорт конфигурации)
```mermaid
sequenceDiagram
    actor User
    participant ConfigLibrary
    participant DataBase@{ "type" : "database" }
    participant OS as System Dialog

    User->>ConfigLibrary: Select config
    User->>ConfigLibrary: Click "Export"
    ConfigLibrary->>DataBase: Extract data
    DataBase-->>ConfigLibrary: Return data
    ConfigLibrary->>OS: Open save dialog
    User->>OS: Select path
    OS->>OS: Write JSON file
    OS-->>ConfigLibrary: Done
```

### 6. Удаление конфигурации (Delete Config)
```mermaid
sequenceDiagram
    actor User
    participant ConfigLibrary
    participant DataBase@{ "type" : "database" }
    participant LocalData@{ "type" : "database" }

    User->>ConfigLibrary: Select config
    User->>ConfigLibrary: Click "Delete"
    ConfigLibrary->>User: Show confirmation dialog ("Are you sure?")
    User->>ConfigLibrary: Confirm delete
    ConfigLibrary->>DataBase: Delete record
    DataBase-->>ConfigLibrary: Delete Done
    ConfigLibrary->>LocalData: Reset/Clear active config
    ConfigLibrary->>ConfigLibrary: Update UI list
```

### 7. Инициализация при запуске (Startup / Load Last Config)
```mermaid
sequenceDiagram
    participant OS as System/User
    participant Main
    participant LocalData@{ "type" : "database" }

    OS->>Main: Launch Application
    Main->>LocalData: Check for last active config
    
    alt Last config exists in LocalData
        LocalData-->>Main: Return last config + session_flag
        
        alt was_session_active == true
            LocalData-->>Main: Config Details
            Main->>Main: Set as Active Current Config
            Main->>Main: UI: Show active state (Tuning enabled)
        else was_session_active == false
            Main->>Main: UI: Show config no changes
        end
        
    else No last config
        Main->>Main: UI: Show config no changes
    end
```


