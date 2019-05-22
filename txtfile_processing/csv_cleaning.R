library(tidyverse)

# Set path to file
path = "D:/concatenated.csv"

# Read in concatenated txt_files
concat <- read_csv(path)

# Remove Spectrogram/Waveform duplication
concat_nodupe <- concat[!duplicated(concat[c(1,3:13)]),]

# Organizing CSV and removing classes with too few datapoints
old_names = c("Sound Type","Begin Time (s)", "End Time (s)")
new_names = c("Class","Start", "End")

succinct <- concat_nodupe %>% 
  group_by(`Sound Type`) %>% 
  filter(n() >= 15) %>%
  drop_na(`Sound Type`) %>%
  select(`Sound Type`, `Begin Time (s)`, `End Time (s)`, Length, Date, File, Selection) %>%
  rename_at(vars(old_names), ~ new_names)

# Displays class counts
succinct %>%
  group_by(Class) %>%
  summarise(n=n()) %>%
  arrange(desc(n))


# Recoding classes  
succinct$Class <- recode(succinct$Class, T = "Opsanus_beta",
       E = "Tursiops_truncatus_Echo", 
       W = "Tursiops_truncatus_Whistle",
       U = "Unknown",
       O = "Cynoscion_nebulosus",
       P = "Bairdiella_chrysoura",
       H = "Ariopsis_felis",
       .default = NA_character_)


# Displaying median class sound lengths
succinct %>%
  group_by(Class) %>%
  summarise(m=median(Length))


# Write cleaned file
write_csv(succinct, "D:/cleaned_concat.csv")

write_csv(head(succinct, 10), "D:/cleaned_concat_practice.csv")
