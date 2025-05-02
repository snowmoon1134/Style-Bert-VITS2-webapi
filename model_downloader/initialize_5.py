import argparse
from model_downloader.downloader import download_jp_extra_pretrained_models


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip_default_models", action="store_true")
    parser.add_argument("--only_infer", action="store_true")
    parser.add_argument(
        "--dataset_root",
        type=str,
        help="Dataset root path (default: Data)",
        default=None,
    )
    parser.add_argument(
        "--assets_root",
        type=str,
        help="Assets root path (default: model_assets)",
        default=None,
    )
    args = parser.parse_args()

    # download_bert_models()

    # if not args.skip_default_models:
    #     download_default_models()
    if not args.only_infer:
    #    download_slm_model()
    #    download_pretrained_models()
         download_jp_extra_pretrained_models()

    # # If configs/paths.yml not exists, create it
    # default_paths_yml = Path("configs/default_paths.yml")
    # paths_yml = Path("configs/paths.yml")
    # if not paths_yml.exists():
    #     shutil.copy(default_paths_yml, paths_yml)

    # if args.dataset_root is None and args.assets_root is None:
    #     return

    # # Change default paths if necessary
    # with open(paths_yml, encoding="utf-8") as f:
    #     yml_data = yaml.safe_load(f)
    # if args.assets_root is not None:
    #     yml_data["assets_root"] = args.assets_root
    # if args.dataset_root is not None:
    #     yml_data["dataset_root"] = args.dataset_root
    # with open(paths_yml, "w", encoding="utf-8") as f:
    #     yaml.dump(yml_data, f, allow_unicode=True)


if __name__ == "__main__":
    main()
