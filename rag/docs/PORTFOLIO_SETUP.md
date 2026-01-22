# Portfolio Data Setup Guide

This guide explains how to set up your portfolio data for the RAG system.

## Overview

The portfolio RAG system allows users to ask questions about your projects, experience, skills, and achievements. The system uses semantic search to find relevant information from a PDF document containing your portfolio data.

## Step 1: Create Your Portfolio PDF

Create a PDF file (`portfolio_data.pdf`) containing your portfolio information. Place it in the `rag/docs/` directory.

### Suggested Structure

Your PDF should include the following sections (you can organize it however you prefer):

1. **Personal Information**
   - Name, title, location
   - Contact information (optional)
   - Professional summary

2. **Work Experience**
   - Company names and roles
   - Duration of employment
   - Key responsibilities
   - Achievements and impact
   - Technologies used

3. **Projects**
   - Project names and descriptions
   - Technologies and tools used
   - Key features and challenges
   - Results and impact
   - Links (GitHub, live demos, etc.)

4. **Skills & Technologies**
   - Programming languages
   - Frameworks and libraries
   - Tools and platforms
   - Databases
   - Cloud services
   - Other relevant skills

5. **Education**
   - Degrees and certifications
   - Relevant coursework
   - Notable achievements

6. **Achievements & Awards**
   - Any notable accomplishments
   - Publications or articles
   - Speaking engagements
   - Open source contributions

### Tips for Better Results

- Be descriptive: Include details about technologies, challenges, and impact
- Use consistent terminology: This helps the semantic search find relevant information
- Include context: Explain what problems you solved and how
- Mention metrics: Include numbers, percentages, or other quantifiable results when possible

## Step 2: Generate Embeddings

Once you have created your `portfolio_data.pdf` file, run the embedding creator script:

```bash
# From the ai-developer-camp directory
python rag/portfolio_embedding_creator.py --file rag/docs/portfolio_data.pdf
```

Or use the default path:

```bash
python rag/portfolio_embedding_creator.py
```

This will:
1. Load and process your PDF
2. Split it into chunks for better search
3. Create embeddings using the HuggingFace model
4. Save the vector store as `portfolio_data` index

The vector store will be saved in `rag/vectorstore/portfolio_data.faiss`.

## Step 3: Verify Setup

After creating the embeddings, you can verify the setup by:

1. Starting the FastAPI backend:
   ```bash
   uv run fastapi dev
   ```

2. Testing the API endpoint:
   ```bash
   curl -X POST http://localhost:8000/pulse/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What projects have you worked on?"}'
   ```

## Updating Your Portfolio

When you update your portfolio PDF:

1. Replace the old `portfolio_data.pdf` with the new one
2. Re-run the embedding creator script:
   ```bash
   python rag/portfolio_embedding_creator.py --file rag/docs/portfolio_data.pdf
   ```

The old vector store will be overwritten with the new embeddings.

## Troubleshooting

### Error: "Failed to load portfolio data"

This means the embeddings haven't been created yet. Run the embedding creator script first.

### Error: "PDF file not found"

Make sure your PDF is in the `rag/docs/` directory, or provide the full path using the `--file` argument.

### Poor search results

- Make sure your PDF contains detailed descriptions
- Try rephrasing your questions
- Ensure the PDF text is readable (not just images)

## Example Questions

Once set up, users can ask questions like:

- "What projects have you worked on?"
- "Tell me about your experience with React"
- "What technologies do you know?"
- "What are your achievements?"
- "Describe your work at [Company Name]"
- "What challenges have you solved in your projects?"

The RAG system will search through your portfolio PDF and provide relevant answers based on the content.

