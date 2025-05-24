from src.database import get_training_data, get_people_data
from src.masking import NameMasker

def main():
    # Get data from databases
    training_data = get_training_data()
    people_data = get_people_data()
    
    if training_data is None or people_data is None:
        print("Error: Could not fetch data from databases")
        return
    
    # Extract name and surname lists
    name_list = people_data['name'].tolist() if 'name' in people_data.columns else []
    surname_list = people_data['surname'].tolist() if 'surname' in people_data.columns else []
    username_list = people_data['username'].tolist() if 'username' in people_data.columns else []
    
    # Create masker instance
    masker = NameMasker(name_list, surname_list, username_list)
    
    # Process test cases from training data
    if 'text' in training_data.columns:
        for idx, row in training_data.iterrows():
            text = row['text']
            masked_text, original_text, masked_words = masker.mask_named_entities(text)
            print(f"\nTest Case {idx + 1}:")
            print(f"Original: {original_text}")
            print(f"Masked  : {masked_text}")
            print("Masked Words:", masked_words)
    else:
        print("Error: Training data does not contain 'text' column")

if __name__ == "__main__":
    main()




