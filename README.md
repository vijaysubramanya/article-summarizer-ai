# Article Summarizer Web App

A modern web application that generates concise summaries of articles using a fine-tuned T5 transformer model. Built with Django (backend) and React (frontend).

## Features

- **AI-Powered Summarization**: Uses a fine-tuned T5 model for high-quality text summarization
- **Customizable Parameters**: Adjust max/min length settings
- **Real-time Statistics**: Shows compression ratio and word counts
- **Modern UI**: Beautiful, responsive design with gradient backgrounds
- **Copy to Clipboard**: Easy summary copying functionality
- **Health Monitoring**: API health check endpoint

## Architecture

```
ArticleSummarizer/
├── backend/                 # Django REST API
│   ├── article_summarizer_project/
│   ├── summarizer/         # Main app with API views
│   ├── requirements.txt    # Python dependencies
│   └── manage.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js         # Main app component
│   │   └── App.css        # Styling
│   └── package.json
├── models/                 # Trained models
│   ├── checkpoint-1878/   # Primary T5 model
│   └── checkpoint-750/    # Alternative model
└── setup.sh               # Quick setup script
```

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Transformers 4.35.0**: Hugging Face transformers library
- **PyTorch 2.0.1**: Deep learning framework
- **T5 Model**: Text-to-text transfer transformer

### Frontend
- **React 18**: Frontend framework
- **Modern CSS**: Gradient backgrounds, animations, responsive design
- **Fetch API**: HTTP requests to backend

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Download Model Checkpoints

**Important**: The trained model checkpoints are not included in this repository due to their large size. You must download them separately:

**Google Drive Link**: [Download Model Checkpoints](https://drive.google.com/drive/folders/1i6eW70gNh1Tbv2eTfb-LP-MLPwwDUzvD?usp=sharing)

1. Download both `checkpoint-750` and `checkpoint-1878` folders from the Google Drive link
2. Place them in the `models/` directory
3. Your final structure should be:
   ```
   models/
   ├── checkpoint-750/
   ├── checkpoint-1878/
   └── README.md
   ```

### Quick Setup
1. Clone the repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```

### Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Usage

1. **Access the Application**: Open http://localhost:3000 in your browser
2. **Enter Article Text**: Paste or type your article in the text area
3. **Adjust Parameters** (Optional): Modify summarization settings
4. **Generate Summary**: Click "Generate Summary" button
5. **View Results**: See the summary with statistics and copy functionality

## API Endpoints

### POST `/api/summarize/`
Summarize article text using the T5 model.

**Request Body:**
```json
{
  "text": "Your article text here...",
  "max_length": 200,
  "min_length": 30,
  "num_beams": 8
}
```

**Response:**
```json
{
  "summary": "Generated summary text...",
  "original_length": 500,
  "summary_length": 150,
  "compression_ratio": 70.0,
  "parameters": {
    "max_length": 200,
    "min_length": 30,
    "num_beams": 8
  }
}
```

### GET `/api/health/`
Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Configuration

### Model Parameters
- **Max Length**: Maximum number of words in summary (default: 200)
- **Min Length**: Minimum number of words in summary (default: 30)
- **Beam Search**: Fixed at 8 beams for optimal quality

### Environment Variables
- `DEBUG`: Django debug mode (default: True)
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Allowed hostnames

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### Frontend Development
```bash
cd frontend
npm start
```

### Model Training
The T5 model was trained on article summarization data and saved in `models/checkpoint-1878/`. The model configuration shows:
- Architecture: T5ForConditionalGeneration
- Model size: 6 layers, 8 heads, 512 dimensions
- Vocabulary size: 32,128 tokens
- Task: Summarization with "summarize: " prefix

## Performance

- **Model Loading**: ~2-3 seconds on first request
- **Inference Time**: ~1-2 seconds for typical articles
- **Memory Usage**: ~2GB RAM for model
- **Supported Text Length**: Up to 512 tokens input

## Troubleshooting

### Common Issues

1. **Model Not Found Error**
   - Ensure `models/checkpoint-1878/` directory exists
   - Check model files are complete

2. **CORS Errors**
   - Verify Django CORS settings
   - Check frontend API URL

3. **Memory Issues**
   - Reduce batch size or model parameters
   - Use GPU if available

4. **Slow Performance**
   - Consider using GPU acceleration
   - Optimize input text length
