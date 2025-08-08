# Models Directory

This directory contains the trained T5 models for article summarization.

## Download Models

**Important**: The model checkpoint folders are not included in this repository due to their large size. You need to download them separately from Google Drive:

**Google Drive Link**: [Download Model Checkpoints](https://drive.google.com/drive/folders/1i6eW70gNh1Tbv2eTfb-LP-MLPwwDUzvD?usp=sharing)

### Setup Instructions:
1. Download both `checkpoint-750` and `checkpoint-1878` folders from the Google Drive link above
2. Extract/place them directly in this `models/` directory
3. Your directory structure should look like:
   ```
   models/
   ├── checkpoint-750/
   │   ├── config.json
   │   ├── model.safetensors
   │   └── ...
   ├── checkpoint-1878/
   │   ├── config.json
   │   ├── model.safetensors
   │   └── ...
   └── README.md
   ```

## Available Models

### `checkpoint-1878/` (Primary Model)
- **Type**: T5ForConditionalGeneration
- **Architecture**: 6 layers, 8 heads, 512 dimensions
- **Vocabulary Size**: 32,128 tokens
- **Task**: Article summarization
- **Prefix**: "summarize: "
- **Status**: Active (used by the web app)

#### Performance Metrics
- **Training Steps**: 1,878
- **Training Loss**: 2.126
- **Training Runtime**: 1,367.89 seconds (~22.8 minutes)
- **Training Speed**: 21.93 samples/second
- **Epochs**: 6.0

#### ROUGE Scores
| Metric | Validation | Test |
|--------|------------|------|
| ROUGE-1 | 31.10% | 30.56% |
| ROUGE-2 | 12.01% | 10.74% |
| ROUGE-L | 22.15% | 22.04% |
| ROUGE-Lsum | 22.20% | 22.10% |

### `checkpoint-750/` (Alternative Model)
- **Type**: T5ForConditionalGeneration
- **Architecture**: 6 layers, 8 heads, 512 dimensions
- **Vocabulary Size**: 32,128 tokens
- **Task**: Article summarization
- **Prefix**: "summarize: "
- **Status**: Backup model

#### Performance Metrics
- **Training Steps**: 750
- **Training Loss**: 2.164
- **Training Runtime**: 161.32 seconds (~2.7 minutes)
- **Training Speed**: 18.60 samples/second
- **Epochs**: 3.0

#### ROUGE Scores
| Metric | Validation | Test |
|--------|------------|------|
| ROUGE-1 | 31.24% | 31.68% |
| ROUGE-2 | 11.85% | 11.72% |
| ROUGE-L | 22.25% | 23.14% |
| ROUGE-Lsum | 22.29% | 23.15% |

## Model Comparison

### Training Comparison
| Metric | Checkpoint-1878 | Checkpoint-750 |
|--------|-----------------|----------------|
| Training Steps | 1,878 | 750 |
| Training Loss | 2.126 | 2.164 |
| Training Time | 22.8 minutes | 2.7 minutes |
| Epochs | 6.0 | 3.0 |

### Performance Comparison
| Metric | Checkpoint-1878 (Test) | Checkpoint-750 (Test) |
|--------|------------------------|----------------------|
| ROUGE-1 | 30.56% | **31.68%** |
| ROUGE-2 | **10.74%** | 11.72% |
| ROUGE-L | 22.04% | **23.14%** |
| ROUGE-Lsum | 22.10% | **23.15%** |

**Note**: Checkpoint-750 shows slightly better ROUGE scores but was trained for fewer steps. Checkpoint-1878 is more thoroughly trained and is used as the primary model.

## Model Configuration

Both models use the same configuration:
- **Model Type**: T5 (Text-to-Text Transfer Transformer)
- **Training**: Fine-tuned for summarization task
- **Input Format**: "summarize: [article_text]"
- **Output**: Concise summary of the input text

## Performance

- **Model Loading Time**: ~2-3 seconds
- **Inference Time**: ~1-2 seconds per article
- **Memory Usage**: ~2GB RAM
- **Max Input Length**: 512 tokens
- **Default Beam Search**: 8 beams

## Switching Models

To use a different model, update the path in `backend/summarizer/views.py`:

```python
checkpoint_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'checkpoint-750')
```

## Model Files

Each checkpoint directory contains:
- `config.json` - Model configuration
- `model.safetensors` - Model weights
- `tokenizer.json` - Tokenizer configuration
- `generation_config.json` - Generation parameters
- `special_tokens_map.json` - Special tokens mapping 