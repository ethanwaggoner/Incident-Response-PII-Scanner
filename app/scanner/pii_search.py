import re
from typing import List, Dict, Union


class PiiSearch:
    def __init__(self, custom_search=None):
        self.custom_search = custom_search

        self.ssn_prefix_list = [
            "",
            " ",
            "Social Security Number",
            "Social Security Number:",
            "SSN",
            "SSN:",
            "SSN#",
            "SSN#:",
            "SSN #",
            "SSN #:",

        ]
        self.ccn_prefix_list = [
            "",
            " ",
            "Credit Card Number",
            "Credit Card Number:",
            "CCN",
            "CCN:",
            "CCN#",
            "CCN#:",
            "CCN #",
            "CCN #:",
        ]

    # verifies if a United States credit card number is legitimate and not a random string of 16 digits
    @staticmethod
    def __verify_us_ccn_luhn(us_ccn: int) -> bool:
        r = [int(ch) for ch in str(us_ccn)][::-1]
        return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0

    # censors the instances of pii with asterisks. censors everything except the last 4 digits, dashes, and prefixes
    @staticmethod
    def __censor_pii(pii_list: List, prefix_list: List) -> List:
        censored_list = []
        prefixes = [prefix + " " for prefix in prefix_list  # isolates prefixes from the pii string
                    for pii in pii_list if prefix in pii]
        to_censor_list = [pii.lstrip(prefix)[:-4] for prefix in prefixes for pii in pii_list]
        uncensored_list = [pii[-4:] for pii in pii_list]

        for censor in to_censor_list:
            censored_chars = ["*" if "-" not in char and " " not in char else "-" for char in censor]
            censored_list.append("".join(censored_chars))

        return [prefix + censored + uncensored for prefix, censored, uncensored in zip(prefixes,
                                                                                       censored_list,
                                                                                       uncensored_list)]

    async def us_ssn(self, data: str) -> List:
        pii_list_list = [re.findall(rf"{prefix}(?:\s|-)?\b\d{{3}}(?:\s|-)?\d{{2}}(?:\s|-)?\d{{4}}\b", data)
                         for prefix in self.ssn_prefix_list]
        pii_list = [item for sublist in pii_list_list for item in sublist]
        return self.__censor_pii(pii_list, self.ssn_prefix_list)

    async def us_ccn(self, data: str) -> List:
        pii_unclean_list_list = [
            re.findall(rf"{prefix}(?:\s|-)?\b\d{{4}}(?:\s|-)?\d{{4}}(?:\s|-)?\d{{4}}(?:\s|-)?\d{{4}}\b", data)
            for prefix in self.ccn_prefix_list]

        pii_unclean_list = [item for sublist in pii_unclean_list_list for item in sublist]

        pii_list = [str(pii) for pii in pii_unclean_list if self.__verify_us_ccn_luhn(
            int(re.sub('[^0-9]', '', pii)))]  # replaces non-digit characters with nothing

        return self.__censor_pii(pii_list, self.ccn_prefix_list)

    async def search_custom(self, data: str) -> List[str]:
        result_list = []

        if self.custom_search:
            for custom in self.custom_search:
                regex = custom.get("regex", "")

                if regex:
                    matches = re.findall(regex, data)
                    if matches:
                        result_list.extend(matches)

        return result_list

