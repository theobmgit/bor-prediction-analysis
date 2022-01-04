import pandas as pd
import random


def parseWithMoneyAndCount(dataframe, colName):
    result = []
    count = []
    gross = []
    for i, record in enumerate(dataframe[colName]):
        for x in record:
            # Lưu kết quả vào mảng tương ứng
            result.append(x)
            gross.append(dataframe['Gross_worldwide'][i])
            count.append(1)
    # Tạo dataFrame
    t = pd.DataFrame({colName: result, 'Total': gross, 'Count': count})
    # Loại bỏ các giá trị trùng nhau và cộng các hàng tương ứng lại
    result1 = t.groupby(colName).sum()
    result1.reset_index(inplace=True)
    t2 = pd.DataFrame({colName: result, 'Mean': gross})
    result2 = t2.groupby(colName).mean()
    result2.reset_index(inplace=True)
    final = result1.merge(result2, on=colName, how='inner')
    t3 = pd.DataFrame({colName: result, 'Median': gross})
    result3 = t3.groupby(colName).median()
    result3.reset_index(inplace=True)
    final = final.merge(result3, on=colName, how='inner')
    return final


class BORFeatureExtractor:
    genreRank = dict()
    castRank = dict()
    crewRank = dict()
    countryRank = dict()
    keywordRank = dict()
    cerRank = dict()
    studioRank = []
    cast10Movies = []
    releases4crew = []
    studios10Larger = []

    def __init__(self):
        pass

    def fitGenre(self, dataSource):
        genre = parseWithMoneyAndCount(dataSource, 'Genre')
        genre = genre[genre['Count'] > 10]
        genre.sort_values(by='Median', ascending=True, inplace=True)
        genre.reset_index(drop=True, inplace=True)
        genreRank = dict()
        for i, row in enumerate(genre['Genre']):
            genreRank[row] = i + 1
        self.genreRank = genreRank

    def fitCast(self, dataSource):
        cast = parseWithMoneyAndCount(dataSource, 'Cast')
        cast.sort_values(by='Count', ascending=False, inplace=True)
        cast10Movies = cast[cast['Count'] > 5]
        cast10Movies.sort_values(by='Mean', ascending=False, inplace=True)
        cast10Movies.reset_index(drop=True, inplace=True)
        cast10Movies.sort_values(by='Mean', ascending=True, inplace=True)
        castRank = dict()
        for i, row in enumerate(cast10Movies['Cast']):
            castRank[row] = i + 1
        self.castRank = castRank
        self.cast10Movies = cast10Movies

    def fitCrew(self, dataSource):
        crew = parseWithMoneyAndCount(dataSource, 'Crew')
        releases4crew = crew[crew['Count'] > 4]
        crewRank = dict()
        releases4crew = releases4crew.sort_values(by='Mean').reset_index(drop=True)
        for i, row in enumerate(releases4crew['Crew']):
            crewRank[row] = i + 1
        self.crewRank = crewRank
        self.releases4crew = releases4crew

    def fitStudio(self, dataSource):
        studio = parseWithMoneyAndCount(dataSource, 'Studios')
        studios10Larger = studio[studio['Count'] > 5]
        studios10Larger.sort_values(by='Mean', ascending=True, inplace=True)
        studioRank = dict()
        for i, row in enumerate(studios10Larger['Studios']):
            studioRank[row] = i + 1
        self.studioRank = studioRank
        self.studios10Larger = studios10Larger

    def fitCountry(self, dataSource):
        country = parseWithMoneyAndCount(dataSource, 'Countries')
        release100Countries = country[country['Count'] >= 100]
        release100Countries = release100Countries.sort_values(by='Mean', ascending=True).reset_index(drop=True)
        countryRank = dict()
        for i, row in enumerate(release100Countries['Countries']):
            countryRank[row] = i + 1  ## Plus 1 in order to release the 0 position for another film
        self.countryRank = countryRank

    def fitKeywords(self, dataSource):
        keyword = parseWithMoneyAndCount(dataSource, 'Keywords')
        count50Keywords = keyword[keyword['Count'] > 20]
        count50Keywords = count50Keywords.sort_values(by='Mean', ascending=True).reset_index(drop=True)
        keywordRank = dict()
        for i, row in enumerate(count50Keywords['Keywords']):
            keywordRank[row] = i + 1  ## Plus 1 in order to release the 0 position for another film
        self.keywordRank = keywordRank

    def fitMPAA(self, dataSource):
        certificate = parseWithMoneyAndCount(dataSource, 'ListOfCertificate')
        certificate = certificate.sort_values(by='Mean', ascending=True).reset_index(drop=True)
        cerRank = dict()
        for i, row in enumerate(certificate['ListOfCertificate']):
            cerRank[row] = i + 1
        self.cerRank = cerRank

    def fit(self, dataSource):
        # Genre
        self.fitGenre(dataSource)
        # Cast
        self.fitCast(dataSource)
        # Crew
        self.fitCrew(dataSource)
        # Studio
        self.fitStudio(dataSource)
        # Country
        self.fitCountry(dataSource)
        # Keywords
        self.fitKeywords(dataSource)
        # MPAA
        self.fitMPAA(dataSource)
        pass

    def extract(self, dataToExtract):
        # Genre
        def getGenreRank(listGenre):
            max = 0
            length = len(listGenre)
            if length == 0:
                length = 1
            for genre in listGenre:
                if genre not in self.genreRank.keys():
                    continue
                max += self.genreRank[genre]
            if max == 0:
                return random.randint(1, 15)
            return max / length

        dataToExtract['GenreRank'] = dataToExtract['Genre'].apply(getGenreRank)

        # SpecialMonth
        def getSpecialMonth(month):
            specialMonth = [5, 6, 7, 11, 12]
            if month in specialMonth:
                return 1
            else:
                return 0

        dataToExtract['SpecialMonth'] = dataToExtract['Release_Month'].apply(getSpecialMonth)

        # Cast
        def getCastsTeamRank(casts):
            total = 0
            for cast in casts:
                if cast not in self.castRank.keys():
                    total += random.randint(1, 200)
                    continue
                total += self.castRank[cast]
            return total

        dataToExtract['CastsRank'] = dataToExtract['Cast'].apply(getCastsTeamRank)
        # NumLeadActor
        cast10Movies = self.cast10Movies
        cast10Movies.sort_values(by='Mean', ascending=False, inplace=True)
        top100Cast = list(cast10Movies['Cast'][0:100])

        def getNumLeadActors(casts):
            total = 0
            for cast in casts:
                if cast in top100Cast:
                    total += 1
            return total

        dataToExtract['NumLeadActors'] = dataToExtract['Cast'].apply(getNumLeadActors)
        # HasTop50Actors
        cast10Movies.sort_values(by='Mean', ascending=False, inplace=True)
        top50Cast = list(cast10Movies['Cast'][0:50])

        def getHasTop30Actors(casts):
            for cast in casts:
                if cast in top50Cast:
                    return 1
            return 0

        dataToExtract['HasTop50Actors'] = dataToExtract['Cast'].apply(getHasTop30Actors)
        # NumCrew
        dataToExtract['NumCrews'] = dataToExtract['Crew'].apply(lambda x: len(x))

        # crewsTeamRank
        def getCrewsTeamRank(crews):
            total = 0
            for crew in crews:
                if crew not in self.crewRank.keys():
                    total += random.randint(1, 100)
                    continue
                total += self.crewRank[crew]
            return total

        dataToExtract['crewsTeamRank'] = dataToExtract['Crew'].apply(getCrewsTeamRank)
        # NumTopCrew
        releases4crew = self.releases4crew
        releases4crew.sort_values(by='Mean', ascending=False, inplace=True)
        top150Crew = list(releases4crew['Crew'][0:150])

        def getNumTopCrew(crews):
            total = 0
            for crew in crews:
                if crew in top150Crew:
                    total += 1
            return total

        dataToExtract['NumTopCrew'] = dataToExtract['Crew'].apply(getNumTopCrew)
        # HasTopCrew
        releases4crew.sort_values(by='Mean', ascending=False, inplace=True)
        top50Crew = list(releases4crew['Crew'][0:50])

        def getHasTopCrew(crews):
            for crew in crews:
                if crew in top50Crew:
                    return 1
            return 0

        dataToExtract['HasTopCrew'] = dataToExtract['Crew'].apply(getHasTopCrew)
        # NumStudios
        dataToExtract['NumStudios'] = dataToExtract['Studios'].apply(lambda x: len(x))

        # StudioRank
        def getStudioRank(studios):
            total = 0
            for studio in studios:
                if studio not in self.studioRank.keys():
                    total += random.randint(1, 200)
                    continue
                total += self.studioRank[studio]
            return total

        dataToExtract['StudioRank'] = dataToExtract['Studios'].apply(getStudioRank)
        # NumTopStudios
        studios10Larger = self.studios10Larger
        studios10Larger.sort_values(by='Mean', ascending=False, inplace=True)
        top100Studios = list(studios10Larger['Studios'][0:100])

        def getNumTopStudios(studios):
            total = 0
            for studio in studios:
                if studio in top100Studios:
                    total += 1
            return total

        dataToExtract['NumTopStudios'] = dataToExtract['Studios'].apply(getNumTopStudios)
        # HasTopStudio
        studios10Larger.sort_values(by='Mean', ascending=False, inplace=True)
        top100Studios = list(studios10Larger['Studios'][0:30])

        def getHasTopStudio(studios):
            for studio in studios:
                if studio in top100Studios:
                    return 1
            return 0

        dataToExtract['HasTopStudio'] = dataToExtract['Studios'].apply(getHasTopStudio)

        # CountryRank
        def getCountryRank(countries):
            max = 0
            for country in countries:
                if country not in self.countryRank.keys():
                    continue
                if self.countryRank[country] > max:
                    max = self.countryRank[country]
            if max == 0:
                max = random.randint(1, 10)
            return max

        dataToExtract['CountryRank'] = dataToExtract['Countries'].apply(getCountryRank)

        # keywordRank
        def getKeywordsRank(keywords):
            max = 0
            for keyword in keywords:
                if keyword not in self.keywordRank.keys():
                    continue
                if self.keywordRank[keyword] > max:
                    max = self.keywordRank[keyword]
            if max == 0:
                max = random.randint(1, 100)
            return max

        dataToExtract['keywordRank'] = dataToExtract['Keywords'].apply(getKeywordsRank)
        #IsEnglish
        dataToExtract['IsEnglish'] = dataToExtract['Languages'].apply(lambda x: 1 if 'English' in x else 0)
        #isAdventure
        dataToExtract['IsAdventure']=dataToExtract['Genre'].apply(lambda x: 1 if 'Adventure' in x else 0)
        #isUnitedStates
        dataToExtract['isUnitedStates'] = dataToExtract['Countries'].apply(lambda x: 1 if "United States" in x else 0)
        #Rated Certificate
        def getCerRank(cers):
            max = 0
            for cer in cers:
                if cer not in self.cerRank.keys():
                    continue
                if self.cerRank[cer] > max:
                    max = self.cerRank[cer]
            return max

        dataToExtract['cerRank'] = dataToExtract['ListOfCertificate'].apply(getCerRank)
        # PG-13
        dataToExtract['PG-13']=dataToExtract['ListOfCertificate'].apply(lambda x: 1 if 'PG-13' in x else 0)
        for index in dataToExtract.columns:
            if type(dataToExtract[index][0]) == str:
                dataToExtract.drop(index, axis=1, inplace=True)
                continue
            if type(dataToExtract[index][0]) == list:
                dataToExtract.drop(index, axis=1, inplace=True)
        # Drop Movie_ID, Rating, Rating_Count
        dataToExtract.drop(['Movie_ID', 'Rating', 'Rating_Count', 'Release_Day', 'Release_Month'], axis=1, inplace=True)
