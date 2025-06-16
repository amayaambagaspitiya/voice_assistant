import os
import re
import pandas as pd

class VehicleSpecsParser:
    def __init__(self, input_folder="src/data/intermediate/specs_output_text", output_file="src/data/final/final_toyota_specsCDcd.csv"):
        self.input_folder = input_folder
        self.output_file = output_file
        self.vehicle_rows = []

    def parse(self):
        for filename in os.listdir(self.input_folder):
            if not filename.endswith("_specs.txt"):
                continue

            parts = filename.replace("_specs.txt", "").split("_")
            year = parts[0]
            vehicle_name = " ".join(parts[1:]).title()
            vehicle_name_clean = self.clean_vehicle_name(vehicle_name)

            file_path = os.path.join(self.input_folder, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            model_info = self._extract_model_names(lines)
            model_names = [name for name, _ in model_info]
            data_by_model = {model: {"engine_specs": engine} for model, engine in model_info}

            self._parse_specs(lines, model_names, data_by_model)

            for model, specs in data_by_model.items():
                row = {
                    "year": year,
                    "vehicle_name": vehicle_name,
                    "vehicle_name_clean": vehicle_name_clean,
                    "model": model
                }
                row.update(specs)
                self.vehicle_rows.append(row)

        self._save_to_csv()
        self._merge_with_additional_data()

    def clean_vehicle_name(self, name):
        name = name.strip().title()
        corrections = {
            "Gr86": "GR86", "Gr Supra": "GR Supra", "Gr Corolla": "GR Corolla",
            "Gr": "GR", "Rav4": "RAV4", "Bz4X": "bZ4X", "I-Force Max": "i-FORCE MAX"
        }
        for wrong, right in corrections.items():
            name = re.sub(rf'\b{wrong}\b', right, name)
        return name

    def _extract_model_names(self, lines):
        model_info = []
        for i, line in enumerate(lines):
            if "Build" in line and i > 1:
                model = lines[i - 2].strip()
                engine = lines[i - 1].strip()
                model_info.append((model, engine))
        return model_info

    def _normalize_key(self, section, attribute):
        attribute = attribute.strip().replace("...", "").replace("…", "").replace("*", "").strip().lower()
        attribute = re.sub(r'\s+', ' ', attribute)
        if "msrp" in attribute:
            attribute = "Base MSRP"
        else:
            attribute = attribute.capitalize()
        return f"{section.title()} - {attribute}"

    def _is_valid_key(self, key):
        invalid_phrases = ["... more", "available as part of an option package", "learn more"]
        return not any(phrase in key.lower() for phrase in invalid_phrases)

    def _parse_specs(self, lines, model_names, data_by_model):
        section = None
        i = 0
        while i < len(lines):
            line = lines[i]

            if line in [
                "MPG/Other/Price", "Interior", "Exterior", "Audio Multimedia", "Connected Services",
                "Safety/Convenience", "Dimensions", "Tires", "Mechanical/Performance",
                "Weights/Capacities", "Packages", "Options", "Warranty Information *"
            ]:
                section = line
                i += 1
                continue

            if section and i + len(model_names) < len(lines):
                attribute = line
                values = lines[i + 1: i + 1 + len(model_names)]

                if all(
                    re.match(r'^\$?[0-9]', val) or 
                    val.startswith("Up to") or 
                    val.endswith("miles") or 
                    "/" in val or 
                    "gal." in val or 
                    "ft." in val or
                    "seats" in val or
                    "months" in val
                    for val in values
                ):
                    normalized_key = self._normalize_key(section, attribute)
                    if self._is_valid_key(normalized_key):
                        for model, val in zip(model_names, values):
                            data_by_model[model][normalized_key] = val
                    i += 1 + len(model_names)
                else:
                    i += 1
            else:
                i += 1

    def _save_to_csv(self):
        df = pd.DataFrame(self.vehicle_rows)
        msrp_col = next((col for col in df.columns if "base msrp" in col.lower()), None)
        selected_cols = ["year", "vehicle_name", "vehicle_name_clean", "model", "engine_specs"]
        if msrp_col:
            selected_cols.append(msrp_col)

        output_dir = os.path.dirname(self.output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        df[selected_cols].to_csv(self.output_file, index=False)
        print(f"✅ Filtered specs saved to '{self.output_file}'")

    def _merge_with_additional_data(self):
        specs_path = self.output_file
        df_specs = pd.read_csv(specs_path)

        # Clean external datasets before merge
        df_seats = pd.read_csv(r"src/data/intermediate/seats_toyota_vehicle_names_by_category.csv")
        df_body = pd.read_csv(r"src/data/intermediate/toyota_vehicle_names_by_category.csv")

        for df in [df_seats, df_body]:
            df["vehicle_name_clean"] = df["vehicle_name"].apply(self.clean_vehicle_name)

        # Merge using cleaned names
        df_merged = df_specs.merge(df_body, on="vehicle_name_clean", how="left").merge(df_seats, on="vehicle_name_clean", how="left")

        output_cleaned = "src/data/final/final_cleaned_toyota_specnew2.csv"
        df_merged.to_csv(output_cleaned, index=False)
        print(f"Final merged dataset saved to '{output_cleaned}'")
