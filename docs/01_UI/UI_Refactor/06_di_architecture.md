classDiagram
    direction TB

    %% --- СЛОЙ 1: Composition Root (Точка сборки) ---
    namespace CompositionRoot {
        class MainPy {
            <<DI Container>>
            +async_main()
        }
    }

    %% --- СЛОЙ 2: UI (Представление) ---
    namespace Layer_UI {
        class MainWindow
        class ConfigDialog
        class SettingsDialog
    }

    %% --- СЛОЙ 3: ViewModels (Состояние и логика UI) ---
    namespace Layer_ViewModels {
        class MainViewModel
        class ConfigViewModel
        class DialogService
    }

    %% --- СЛОЙ 4: Application Services (Бизнес-логика) ---
    namespace Layer_Services {
        class TelemetryManager
        class ConfigStateManager
        class ConfigValidatorService
    }

    %% --- СЛОЙ 5: Infrastructure & Core (Внешний мир) ---
    namespace Layer_Infrastructure {
        class RealCoreFacade
        class LocalConfigRepository
        class UdpListener
    }

    %% === ВЛАДЕНИЕ И ИНЖЕКЦИЯ (Кто кого создает и использует) ===

    %% Сборка в main.py
    MainPy ..> TelemetryManager : creates
    MainPy ..> LocalConfigRepository : creates
    MainPy ..> ConfigStateManager : creates (injects Repo)
    MainPy ..> MainViewModel : creates (injects Telemetry)
    MainPy ..> ConfigViewModel : creates (injects ConfigState)
    MainPy ..> DialogService : creates (injects VMs)
    MainPy ..> MainWindow : creates (injects MainVM & DialogService)

    %% Использование в рантайме (Стрелки владения)
    MainWindow *-- MainViewModel : uses
    MainWindow *-- DialogService : uses
    
    DialogService *-- ConfigViewModel : opens dialogs with
    
    MainViewModel *-- TelemetryManager : gets telemetry / starts session
    
    TelemetryManager *-- RealCoreFacade : uses ICoreFacade
    RealCoreFacade *-- UdpListener : runs in background thread
    
    ConfigViewModel *-- ConfigStateManager : validates & saves
    ConfigViewModel *-- ConfigValidatorService : uses
    ConfigStateManager *-- LocalConfigRepository : reads/writes JSON