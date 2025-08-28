import os

def test_file_operations():
    """Test file operations in the current environment."""
    try:
        # Test file creation
        with open("test_output.txt", "w") as f:
            f.write("Testing file operations\n")
            f.write(f"Current directory: {os.getcwd()}\n")
        
        # Test directory creation
        test_dir = "test_directory"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            with open(os.path.join(test_dir, "test_file.txt"), "w") as f:
                f.write("Test file in directory\n")
        
        print("File operations test completed successfully")
        return True
        
    except Exception as e:
        print(f"File operations test failed: {e}")
        return False

if __name__ == "__main__":
    test_file_operations()
