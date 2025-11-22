class Band:
    def __init__(self, name):
        self.name = name
        self.members = {}  
        self.songs = []

    def add_member(self, name, role):
        """
        Add a new member with their role.
        """
        self.members[name] = role

    def remove_member(self, name):
        """
        Remove a member by name.
        """
        if name in self.members:
            del self.members[name]

    def release_song(self, song_title):
        """
        Add a new song.
        """
        self.songs.append(song_title)

    def list_members(self):
        """
        Print all members with roles.
        """
        for name, role in self.members.items():
            print(f"{name} - {role}")

    def list_songs(self):
        """
        Print all songs released by the band.
        """
        print("Songs:")
        for song in self.songs:
            print(song)


if __name__ == "__main__":
    band = Band("Wandering Monks")
    
    band.add_member("Punky Monk", "singer")
    band.add_member("Funky Monk", "bassist")
    band.add_member("Clunky Monk", "guitarist")
    band.add_member("Chunky Monk", "drummer")

    band.release_song("One with nothing")
    band.release_song("Winston")

    band.remove_member("Punky Monk")
    band.add_member("Junky Monk", "singer")

    band.list_members()
    print()
    band.list_songs()