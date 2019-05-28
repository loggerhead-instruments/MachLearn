import os
import random
import shutil

whistle_directory = r'C:\Users\Austin\Documents\Academics\NCF\Semester_2\Loggerhead\practice\data_split_practice\Original_data\whistle'
no_whistle_directory = r'C:\Users\Austin\Documents\Academics\NCF\Semester_2\Loggerhead\practice\data_split_practice\Original_data\no_whistle'
my_split_dir = r'C:\Users\Austin\Documents\Academics\NCF\Semester_2\Loggerhead\practice\data_split_practice\Original_data\splits'




def split_data(class_1_directory, class_2_directory, split_directory, binary_name, set_seed=223):

    if os.path.isdir(whistle_directory) and os.path.isdir(no_whistle_directory):
        os.makedirs(split_directory + '/train/' + str(binary_name))
        os.makedirs(split_directory + '/train/' + 'no_' + str(binary_name))
        os.makedirs(split_directory + '/val/' + str(binary_name))
        os.makedirs(split_directory + '/val/' + 'no_' + str(binary_name))
        os.makedirs(split_directory + '/test/' + str(binary_name))
        os.makedirs(split_directory + '/test/' + 'no_' + str(binary_name))

        # Obtain files from class 1 and class 2:
        class_1_files = os.listdir(class_1_directory)
        class_2_files = os.listdir(class_2_directory)

        class_1_files.sort()
        class_2_files.sort()

        random.seed(set_seed)

        random.shuffle(class_1_files)
        random.shuffle(class_2_files)

        split_1 = int(0.8 * len(class_1_files))
        split_2 = int(0.9 * len(class_1_files))
        train_filenames = class_1_files[:split_1]
        dev_filenames = class_1_files[split_1:split_2]
        test_filenames = class_1_files[split_2:]

        for item in train_filenames:
            s = os.path.join(class_1_directory, item)
            d = os.path.join(split_directory + '/train/' + str(binary_name), item)

            shutil.copy(s, d)

        for item in dev_filenames:
            s = os.path.join(class_1_directory, item)
            d = os.path.join(split_directory + '/val/' + str(binary_name), item)

            shutil.copy(s, d)

        for item in test_filenames:
            s = os.path.join(class_1_directory, item)
            d = os.path.join(split_directory + '/test/' + str(binary_name), item)

            shutil.copy(s, d)

        split_1 = int(0.8 * len(class_2_files))
        split_2 = int(0.9 * len(class_2_files))
        train_filenames = class_2_files[:split_1]
        dev_filenames = class_2_files[split_1:split_2]
        test_filenames = class_2_files[split_2:]

        for item in train_filenames:
            s = os.path.join(class_2_directory, item)
            d = os.path.join(split_directory + '/train/' + 'no_' + str(binary_name), item)

            shutil.copy(s, d)

        for item in dev_filenames:
            s = os.path.join(class_2_directory, item)
            d = os.path.join(split_directory + '/val/' + 'no_' + str(binary_name), item)

            shutil.copy(s, d)

        for item in test_filenames:
            s = os.path.join(class_2_directory, item)
            d = os.path.join(split_directory + '/test/' + 'no_' + str(binary_name), item)

            shutil.copy(s, d)

    else:
        print("ERROR: One or both of the data directories do not exist!")
        return -1


split_data(whistle_directory, no_whistle_directory, my_split_dir, "whistle")