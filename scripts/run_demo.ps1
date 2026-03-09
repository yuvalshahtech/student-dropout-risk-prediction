# ============================================================
# Student Dropout Risk Prediction - AI/ML Demo Runner
# ============================================================

$ErrorActionPreference = "Stop"

Clear-Host

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Student Dropout Risk Prediction - AI/ML Demo Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------------------------
# Move to project root
# ------------------------------------------------------------

$projectRoot = Get-Location
Write-Host "Project Root: $projectRoot"
Write-Host ""

# ------------------------------------------------------------
# Step 1: Setup virtual environment
# ------------------------------------------------------------

Write-Host "Step 1: Preparing virtual environment..." -ForegroundColor Yellow

$venvFolder = ".venv"
$activateScript = ".\.venv\Scripts\Activate.ps1"

if (!(Test-Path $activateScript)) {

    Write-Host "Virtual environment missing or broken." -ForegroundColor Yellow
    Write-Host "Recreating environment..." -ForegroundColor Yellow

    if (Test-Path $venvFolder) {
        Remove-Item -Recurse -Force $venvFolder
    }

    python -m venv .venv

}

if (!(Test-Path $activateScript)) {
    Write-Host "ERROR: Virtual environment creation failed." -ForegroundColor Red
    exit 1
}

& $activateScript

Write-Host "Virtual environment activated." -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------
# Step 2: Install dependencies
# ------------------------------------------------------------

Write-Host "Step 2: Installing dependencies..." -ForegroundColor Yellow

python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Dependencies installed." -ForegroundColor Green
Write-Host ""

# ------------------------------------------------------------
# Step 3: Check model
# ------------------------------------------------------------

Write-Host "Step 3: Checking model artifacts..." -ForegroundColor Yellow

$modelPath = ".\models\logistic_tuned\model.joblib"

if (!(Test-Path $modelPath)) {

    Write-Host "WARNING: Model not found." -ForegroundColor Yellow
    Write-Host "Run training first:"
    Write-Host "python -m student_management.training --data data/sample_students.csv"
    Write-Host ""

    Read-Host "Press ENTER to continue anyway"
}
else {

    Write-Host "Model artifacts found." -ForegroundColor Green
}

Write-Host ""

# ------------------------------------------------------------
# Step 4: Launch Streamlit
# ------------------------------------------------------------

Write-Host "Step 4: Launching Streamlit demo..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Open in browser: http://localhost:8501"
Write-Host "Press CTRL+C to stop"
Write-Host ""

streamlit run streamlit_app.py

Write-Host ""
Write-Host "Demo closed."
Write-Host "============================================================"