Function ParseEncodedString(encodedStr As String, param As String) As String
    ' Create the RegExp object
    Dim regEx As Object
    Set regEx = CreateObject("VBScript.RegExp")
    
    ' Variables to store extracted values
    Dim PC As String
    Dim SN As String
    Dim LOTE As String
    Dim CAD As String
    
    ' Define and execute regex pattern for PC
    regEx.Pattern = "01[01](8\d{8,}?)(10|17|21|$)"
    Set Matches = regEx.Execute(encodedStr)
    If Matches.Count > 0 Then PC = Matches(0).SubMatches(0)

    ' Define and execute regex pattern for SN
    regEx.Pattern = "21(\w{8,}?)(10|17|71|$)"
    Set Matches = regEx.Execute(encodedStr)
    If Matches.Count > 0 Then SN = Matches(0).SubMatches(0)

    ' Define and execute regex pattern for LOTE
    regEx.Pattern = "(?<!^0)10(\w{3,}?)(?=21|17|71|$)"
    Set Matches = regEx.Execute(encodedStr)
    If Matches.Count > 0 Then LOTE = Matches(0).SubMatches(0)

    ' Define and execute regex pattern for CAD
    regEx.Pattern = "17(\d{4})(21|10|30|31|71)"
    Set Matches = regEx.Execute(encodedStr)
    If Matches.Count > 0 Then CAD = Matches(0).SubMatches(0)

    ' Return the appropriate parameter based on the user's input
    Select Case UCase(param)
        Case "PC"
            ParseEncodedString = PC
        Case "SN"
            ParseEncodedString = SN
        Case "LOTE"
            ParseEncodedString = LOTE
        Case "CAD"
            ParseEncodedString = CAD
        Case Else
            ParseEncodedString = "Invalid parameter"
    End Select
End Function

