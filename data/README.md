# Dataset Instructions

## Required File

Place your resume dataset CSV file here with the name:
```
resume_dataset.csv
```

## Required Columns

Your CSV must contain these exact columns:

1. **Resume_str** - The full text content of the resume
2. **Category** - The job category/domain (e.g., "Data Science", "Web Development", "Software Engineer")

## Example Structure

```csv
Resume_str,Category
"John Doe. Python developer with 5 years experience in machine learning...","Data Science"
"Jane Smith. Full stack developer proficient in React and Node.js...","Web Development"
"Bob Johnson. Software engineer with expertise in Java and Spring...","Software Engineer"
```

## Supported Categories

The system works best with these categories (but supports others too):
- Data Science
- Web Development
- Software Engineer
- Mobile Development
- DevOps
- Business Analyst
- Network Engineer
- Database Administrator
- Cyber Security
- Cloud Architect
- Machine Learning
- Project Manager
- QA Engineer
- UI/UX Designer
- Technical Support

## Dataset Tips

1. **Size**: Minimum 100 resumes recommended, 500+ ideal
2. **Quality**: Ensure Resume_str contains actual resume text (not just keywords)
3. **Balance**: Try to have balanced categories (similar number of resumes per category)
4. **Cleaning**: Remove any duplicate resumes before training
5. **Format**: Save as UTF-8 encoded CSV

## Where to Get Datasets

You can find resume datasets on:
- Kaggle (search for "resume dataset")
- GitHub repositories
- Academic datasets
- Your own collection (with proper anonymization)

## After Placing Dataset

Once you've placed `resume_dataset.csv` in this folder:

```bash
# Go back to project root
cd ..

# Run the training script
python train_model.py
```

The script will:
1. Load and validate your dataset
2. Preprocess the text
3. Train the ML models
4. Save models to `models/` folder
5. Show training statistics

## Troubleshooting

**"Dataset not found" error:**
- Ensure file is named exactly `resume_dataset.csv`
- Check it's in the `data/` folder
- Verify the file isn't empty

**"Missing columns" error:**
- Open CSV and verify column names are exactly `Resume_str` and `Category`
- Check for typos or extra spaces in column names

**"No text extracted" error:**
- Verify Resume_str column contains actual resume text
- Check that text is not just empty strings
