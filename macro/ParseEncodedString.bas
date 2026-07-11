Attribute VB_Name = "DataMatrix2CodesModule"
Option Explicit

Private Const GROUP_SEPARATOR As String = vbNullChar

Public Function ParseEncodedString(encodedStr As Variant, param As Variant) As String
    Dim parsed As String
    Dim cleanParam As String

    On Error GoTo FunctionError
    parsed = ParseDataMatrix(encodedStr)
    cleanParam = UCase$(Trim$(SafeText(param)))

    Select Case cleanParam
        Case "PC"
            ParseEncodedString = CandidatePart(parsed, 0)
        Case "SN"
            ParseEncodedString = CandidatePart(parsed, 1)
        Case "LOTE"
            ParseEncodedString = CandidatePart(parsed, 2)
        Case "CAD"
            ParseEncodedString = CandidatePart(parsed, 3)
        Case "STATUS"
            ParseEncodedString = CandidatePart(parsed, 6)
        Case "CONFIDENCE"
            ParseEncodedString = CandidatePart(parsed, 7)
        Case "HAS_GS"
            ParseEncodedString = CandidatePart(parsed, 8)
        Case "EXPLAIN"
            ParseEncodedString = CandidatePart(parsed, 9)
        Case Else
            ParseEncodedString = "Invalid parameter"
    End Select

    Exit Function

FunctionError:
    If UCase$(Trim$(SafeText(param))) = "EXPLAIN" Then
        ParseEncodedString = "VBA error " & CStr(Err.Number) & ": " & Err.Description
    Else
        ParseEncodedString = ""
    End If
End Function

Public Function ParseEncodedStatus(encodedStr As Variant) As String
    ParseEncodedStatus = ParseEncodedString(encodedStr, "STATUS")
End Function

Public Sub DataMatrix2Codes()
    SetupDataMatrixWorksheet
End Sub

Public Sub PrepareDataMatrixWorksheet()
    Dim ws As Worksheet
    Dim headers As Variant
    Dim i As Long

    On Error GoTo PrepareError

    Set ws = ActiveSheet
    headers = Array("CODE", "PC", "SN", "LOTE", "CAD", "STATUS", "CONFIDENCE", "HAS_GS", "EXPLAIN")

    ws.Range(ws.Columns(1), ws.Columns(9)).NumberFormat = "@"
    For i = LBound(headers) To UBound(headers)
        ws.Cells(1, i + 1).Value = headers(i)
        ws.Cells(1, i + 1).Font.Bold = True
        ws.Cells(1, i + 1).Interior.Color = RGB(31, 78, 121)
        ws.Cells(1, i + 1).Font.Color = RGB(255, 255, 255)
    Next i
    ws.Columns(1).ColumnWidth = 60
    ws.Cells(2, 1).Select

    MsgBox "Scanner sheet is ready. Columns A:I are formatted as text. Scan raw DataMatrix strings under CODE, then run DataMatrix2Codes again.", vbInformation
    Exit Sub

PrepareError:
    MsgBox "Could not prepare the scanner sheet." & vbCrLf & _
           "VBA error " & CStr(Err.Number) & ": " & Err.Description, vbExclamation
End Sub

Public Sub SetupDataMatrixWorksheet()
    Dim ws As Worksheet
    Dim headers As Variant
    Dim lastRow As Long
    Dim i As Long
    Dim rowIndex As Long
    Dim parsed As String
    Dim tableRange As Range
    Dim stage As String

    On Error GoTo SetupError
    stage = "select active worksheet"
    Set ws = ActiveSheet
    headers = Array("CODE", "PC", "SN", "LOTE", "CAD", "STATUS", "CONFIDENCE", "HAS_GS", "EXPLAIN")

    stage = "format scanner and output columns"
    ws.Range(ws.Columns(1), ws.Columns(9)).NumberFormat = "@"

    stage = "write headers"
    For i = LBound(headers) To UBound(headers)
        ws.Cells(1, i + 1).Value = headers(i)
        ws.Cells(1, i + 1).Font.Bold = True
        ws.Cells(1, i + 1).Interior.Color = RGB(31, 78, 121)
        ws.Cells(1, i + 1).Font.Color = RGB(255, 255, 255)
    Next i

    stage = "find last scanner row"
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    If lastRow < 2 Then
        ws.Cells(2, 1).Select
        MsgBox "Scanner sheet is ready. Columns A:I are formatted as text. Scan raw DataMatrix strings under CODE, then run DataMatrix2Codes again to convert them.", vbInformation
        Exit Sub
    End If

    stage = "parse scanner rows"
    For rowIndex = 2 To lastRow
        parsed = ParseDataMatrix(ws.Cells(rowIndex, 1).Value)
        ws.Cells(rowIndex, 2).Value = CandidatePart(parsed, 0)
        ws.Cells(rowIndex, 3).Value = CandidatePart(parsed, 1)
        ws.Cells(rowIndex, 4).Value = CandidatePart(parsed, 2)
        ws.Cells(rowIndex, 5).Value = CandidatePart(parsed, 3)
        ws.Cells(rowIndex, 6).Value = CandidatePart(parsed, 6)
        ws.Cells(rowIndex, 7).Value = CandidatePart(parsed, 7)
        ws.Cells(rowIndex, 8).Value = CandidatePart(parsed, 8)
        ws.Cells(rowIndex, 9).Value = CandidatePart(parsed, 9)
    Next rowIndex

    stage = "fit columns"
    Set tableRange = ws.Range(ws.Cells(1, 1), ws.Cells(lastRow, UBound(headers) + 1))
    tableRange.Columns.AutoFit

    stage = "apply review colors"
    ApplyDataMatrixFormatting ws, lastRow

    MsgBox "DataMatrix values and review colors were applied.", vbInformation
    Exit Sub

SetupError:
    MsgBox "DataMatrix setup failed while trying to " & stage & "." & vbCrLf & _
           "VBA error " & CStr(Err.Number) & ": " & Err.Description, vbExclamation
End Sub

Public Sub DiagnoseDataMatrixActiveCell()
    Dim parsed As String
    Dim rawText As String
    Dim message As String

    On Error GoTo DiagnoseError

    rawText = SafeText(ActiveCell.Value)
    parsed = ParseDataMatrix(ActiveCell.Value)

    message = "Active cell: " & ActiveCell.Address(False, False) & vbCrLf & _
              "Excel value type: " & TypeName(ActiveCell.Value) & vbCrLf & _
              "Text length: " & CStr(Len(rawText)) & vbCrLf & _
              "STATUS: " & CandidatePart(parsed, 6) & vbCrLf & _
              "PC: " & CandidatePart(parsed, 0) & vbCrLf & _
              "SN: " & CandidatePart(parsed, 1) & vbCrLf & _
              "LOTE: " & CandidatePart(parsed, 2) & vbCrLf & _
              "CAD: " & CandidatePart(parsed, 3) & vbCrLf & _
              "EXPLAIN: " & CandidatePart(parsed, 9)

    MsgBox message, vbInformation
    Exit Sub

DiagnoseError:
    MsgBox "Diagnostic failed with VBA error " & CStr(Err.Number) & ": " & Err.Description, vbExclamation
End Sub

Public Sub RunDataMatrixSelfTest()
    Dim codes(1 To 17) As String
    Dim expected(1 To 17, 1 To 4) As String
    Dim i As Long
    Dim failures As String
    Dim parsed As String

    codes(1) = "010847000654766321ANT7T3KA311726033110231853"
    expected(1, 1) = "8470006547663": expected(1, 2) = "ANT7T3KA31": expected(1, 3) = "231853": expected(1, 4) = "2603"
    codes(2) = "010843523230050521TNCW7D02MD6A10V4TP1172505317128342594"
    expected(2, 1) = "8435232300505": expected(2, 2) = "TNCW7D02MD6A": expected(2, 3) = "V4TP1": expected(2, 4) = "2505"
    codes(3) = "01084700069709041726053110V00221SRK819FGA8FN1X"
    expected(3, 1) = "8470006970904": expected(3, 2) = "SRK819FGA8FN1X": expected(3, 3) = "V002": expected(3, 4) = "2605"
    codes(4) = "010847000694711121JG4FGW0FWM000A10147016010117250930"
    expected(4, 1) = "8470006947111": expected(4, 2) = "JG4FGW0FWM000A": expected(4, 3) = "1470160101": expected(4, 4) = "2509"
    codes(5) = "010847000700588921016155286963841726043010TBLZ"
    expected(5, 1) = "8470007005889": expected(5, 2) = "01615528696384": expected(5, 3) = "TBLZ": expected(5, 4) = "2604"
    codes(6) = "0108470006709382211082464896195410NB226517260430"
    expected(6, 1) = "8470006709382": expected(6, 2) = "10824648961954": expected(6, 3) = "NB2265": expected(6, 4) = "2604"
    codes(7) = "01084700070382831725013110DK17721397997676722"
    expected(7, 1) = "8470007038283": expected(7, 2) = "397997676722": expected(7, 3) = "DK177": expected(7, 4) = "2501"
    codes(8) = "010847000670166921CWNF2V6PEG7GE17270430103805"
    expected(8, 1) = "8470006701669": expected(8, 2) = "CWNF2V6PEG7GE": expected(8, 3) = "3805": expected(8, 4) = "2704"
    codes(9) = "010847000698208221F065AWAAVW71269820821725013110205437"
    expected(9, 1) = "8470006982082": expected(9, 2) = "F065AWAAVW": expected(9, 3) = "205437": expected(9, 4) = "2501"
    codes(10) = "010847000700681721PE42EEADPA9HW41728033110V067127006817"
    expected(10, 1) = "8470007006817": expected(10, 2) = "PE42EEADPA9HW4": expected(10, 3) = "V06": expected(10, 4) = "2803"
    codes(11) = "0108410840049947217HGPVAACCEH110T49172503317129577537"
    expected(11, 1) = "8410840049947": expected(11, 2) = "7HGPVAACCEH1": expected(11, 3) = "T49": expected(11, 4) = "2503"
    codes(12) = "01189010791063361726103110HFZ022058218058271392047127035497"
    expected(12, 1) = "18901079106336": expected(12, 2) = "805827139204": expected(12, 3) = "HFZ022058": expected(12, 4) = "2610"
    codes(13) = "0108470007210764211002664707361010A59112B17260430"
    expected(13, 1) = "8470007210764": expected(13, 2) = "10026647073610": expected(13, 3) = "A59112B": expected(13, 4) = "2604"
    codes(14) = "01084365715201041721010010LETRASGRANDESGS21letraspequenasGS7127166559"
    expected(14, 1) = "8436571520104": expected(14, 2) = "letraspequenas": expected(14, 3) = "LETRASGRANDES": expected(14, 4) = "2101"
    codes(15) = "01084365715201041721010010////_ _ _ _GS21----....GS7127166559"
    expected(15, 1) = "8436571520104": expected(15, 2) = "----....": expected(15, 3) = "////_ _ _ _": expected(15, 4) = "2101"
    codes(16) = "01084365715201041721010010ZZZZZGS21YYYYYGS7127166559"
    expected(16, 1) = "8436571520104": expected(16, 2) = "YYYYY": expected(16, 3) = "ZZZZZ": expected(16, 4) = "2101"
    codes(17) = "010843657152010417210100101234567890GS21ABCDEFGS7127166559"
    expected(17, 1) = "8436571520104": expected(17, 2) = "ABCDEF": expected(17, 3) = "1234567890": expected(17, 4) = "2101"

    For i = 1 To 17
        parsed = ParseDataMatrix(codes(i))
        If CandidatePart(parsed, 0) <> expected(i, 1) Or _
           CandidatePart(parsed, 1) <> expected(i, 2) Or _
           CandidatePart(parsed, 2) <> expected(i, 3) Or _
           CandidatePart(parsed, 3) <> expected(i, 4) Or _
           CandidatePart(parsed, 6) <> "OK" Then
            failures = failures & "Row " & CStr(i) & " failed." & vbCrLf
        End If
    Next i

    If Len(failures) = 0 Then
        MsgBox "All DataMatrix parser self-tests passed.", vbInformation
    Else
        MsgBox failures, vbExclamation
    End If
End Sub

Private Function ParseDataMatrix(encodedStr As Variant) As String
    Dim value As String
    Dim candidates As Collection
    Dim best As String
    Dim bestScore As Long
    Dim i As Long
    Dim score As Long
    Dim ties As New Collection
    Dim result As String

    value = NormalizeInput(encodedStr)
    If Len(value) = 0 Then
        ParseDataMatrix = CandidateText("", "", "", "", 0, "", "UNPARSED", "0", BoolText(HasGroupSeparator(encodedStr)), "No scan was provided.")
        Exit Function
    End If

    Set candidates = WalkCandidates(value, 1)
    If candidates.Count = 0 Then
        ParseDataMatrix = CandidateText("", "", "", "", 0, "", "UNPARSED", "0", BoolText(HasGroupSeparator(encodedStr)), "The scan could not be decoded. Check the scanner input or enter the values manually.")
        Exit Function
    End If

    best = candidates(1)
    bestScore = ScoreCandidate(best)
    For i = 2 To candidates.Count
        score = ScoreCandidate(candidates(i))
        If score > bestScore Then
            best = candidates(i)
            bestScore = score
        End If
    Next i

    For i = 1 To candidates.Count
        If ScoreCandidate(candidates(i)) = bestScore Then ties.Add candidates(i)
    Next i

    result = ResolveTies(best, ties, HasGroupSeparator(encodedStr), candidates)
    ParseDataMatrix = result
End Function

Private Function HasGroupSeparator(value As Variant) As Boolean
    Dim text As String

    text = SafeText(value)
    HasGroupSeparator = (InStr(1, text, Chr$(29), vbBinaryCompare) > 0 Or _
                         InStr(1, text, "<GS>", vbTextCompare) > 0 Or _
                         InStr(1, text, "{GS}", vbTextCompare) > 0 Or _
                         HasVisibleSeparatorBeforeAi(text))
End Function

Private Function NormalizeInput(value As Variant) As String
    Dim text As String
    Dim i As Long
    Dim ch As String
    Dim result As String

    text = Trim$(SafeText(value))
    If Left$(text, 3) = "]d2" Then text = Mid$(text, 4)
    text = Replace$(text, "<GS>", Chr$(29))
    text = Replace$(text, "{GS}", Chr$(29))

    For i = 1 To Len(text)
        If Mid$(text, i, 2) = "GS" And IsAiMarkerAt(text, i + 2) Then
            result = result & GROUP_SEPARATOR
            i = i + 1
        ElseIf (Mid$(text, i, 1) = "|" Or Mid$(text, i, 1) = "'") And IsAiMarkerAt(text, i + 1) Then
            result = result & GROUP_SEPARATOR
        Else
            ch = Mid$(text, i, 1)
            If ch = Chr$(29) Then
                result = result & GROUP_SEPARATOR
            ElseIf ch <> vbTab And ch <> vbCr And ch <> vbLf Then
                result = result & ch
            End If
        End If
    Next i

    NormalizeInput = result
End Function

Private Function HasVisibleSeparatorBeforeAi(text As String) As Boolean
    Dim i As Long

    For i = 1 To Len(text)
        If Mid$(text, i, 2) = "GS" And IsAiMarkerAt(text, i + 2) Then
            HasVisibleSeparatorBeforeAi = True
            Exit Function
        End If
        If (Mid$(text, i, 1) = "|" Or Mid$(text, i, 1) = "'") And IsAiMarkerAt(text, i + 1) Then
            HasVisibleSeparatorBeforeAi = True
            Exit Function
        End If
    Next i
End Function

Private Function IsAiMarkerAt(text As String, pos As Long) As Boolean
    Dim marker As String

    If pos < 1 Or pos + 1 > Len(text) Then Exit Function
    marker = Mid$(text, pos, 2)
    Select Case marker
        Case "01", "10", "17", "21", "71"
            IsAiMarkerAt = True
    End Select
End Function

Private Function SafeText(value As Variant) As String
    On Error GoTo SafeTextError

    If IsError(value) Then Exit Function
    If IsNull(value) Then Exit Function
    If IsEmpty(value) Then Exit Function

    If IsObject(value) Then
        If TypeName(value) = "Range" Then
            SafeText = SafeText(value.Cells(1, 1).Value)
        End If
        Exit Function
    End If

    SafeText = CStr(value)
    Exit Function

SafeTextError:
    SafeText = ""
End Function

Private Function WalkCandidates(value As String, pos As Long) As Collection
    Dim results As New Collection
    Dim rest As Collection
    Dim item As Variant
    Dim gtin As String
    Dim expiry As String
    Dim nhrn As String
    Dim added As String

    If pos > Len(value) Then
        results.Add CandidateText("", "", "", "", 0, "", "")
        Set WalkCandidates = results
        Exit Function
    End If

    If Mid$(value, pos, 1) = GROUP_SEPARATOR Then
        Set WalkCandidates = WalkCandidates(value, pos + 1)
        Exit Function
    End If

    If Mid$(value, pos, 2) = "01" Then
        gtin = Mid$(value, pos + 2, 14)
        If Len(gtin) = 14 And IsDigits(gtin) Then
            Set rest = WalkCandidates(value, pos + 16)
            For Each item In rest
                added = WithField(CStr(item), "PC", NormalizeGtin(gtin))
                If Len(added) > 0 Then results.Add added
            Next item
        End If
    End If

    If Mid$(value, pos, 2) = "17" Then
        expiry = Mid$(value, pos + 2, 6)
        If Len(expiry) = 6 And IsDigits(expiry) And IsValidExpiry(expiry) Then
            Set rest = WalkCandidates(value, pos + 8)
            For Each item In rest
                added = WithField(CStr(item), "CAD", Left$(expiry, 4))
                If Len(added) > 0 Then results.Add added
            Next item
        End If
    End If

    If Mid$(value, pos, 2) = "71" Then
        nhrn = Mid$(value, pos + 2, 8)
        If Len(nhrn) = 8 And IsDigits(nhrn) Then
            Set rest = WalkCandidates(value, pos + 10)
            For Each item In rest
                results.Add WithIgnored71(CStr(item))
            Next item
        End If
    End If

    If Mid$(value, pos, 2) = "10" Then AddVariableCandidates results, value, pos + 2, "LOTE", 3, 20
    If Mid$(value, pos, 2) = "21" Then AddVariableCandidates results, value, pos + 2, "SN", 1, 20

    If results.Count = 0 Then results.Add CandidateText("", "", "", "", 0, Mid$(value, pos), "")
    Set WalkCandidates = results
End Function

Private Sub AddVariableCandidates(results As Collection, value As String, startPos As Long, fieldName As String, minLen As Long, maxLen As Long)
    Dim limit As Long
    Dim sep As Long
    Dim length As Long
    Dim itemValue As String
    Dim rest As Collection
    Dim item As Variant
    Dim added As String

    limit = maxLen
    If Len(value) - startPos + 1 < limit Then limit = Len(value) - startPos + 1

    sep = InStr(startPos, value, GROUP_SEPARATOR, vbBinaryCompare)
    If sep > 0 And sep - startPos <= maxLen Then
        length = sep - startPos
        If length >= minLen Then
            itemValue = Mid$(value, startPos, length)
            If IsVariableValue(itemValue) Then
                Set rest = WalkCandidates(value, sep + 1)
                For Each item In rest
                    added = WithField(CStr(item), fieldName, itemValue)
                    If Len(added) > 0 Then results.Add added
                Next item
            End If
        End If
        Exit Sub
    End If

    For length = minLen To limit
        itemValue = Mid$(value, startPos, length)
        If IsVariableValue(itemValue) Then
            Set rest = WalkCandidates(value, startPos + length)
            For Each item In rest
                added = WithField(CStr(item), fieldName, itemValue)
                If Len(added) > 0 Then results.Add added
            Next item
        End If
    Next length
End Sub

Private Function ResolveTies(best As String, ties As Collection, hasGs As Boolean, allCandidates As Collection) As String
    Dim pc As String
    Dim sn As String
    Dim lote As String
    Dim cad As String
    Dim status As String
    Dim explain As String
    Dim item As Variant

    pc = CandidatePart(best, 0)
    sn = CandidatePart(best, 1)
    lote = CandidatePart(best, 2)
    cad = CandidatePart(best, 3)
    status = "OK"
    explain = IIf(hasGs, "Code read correctly with scanner separators.", "Code read correctly.")
    If Len(pc) = 0 Or Len(sn) = 0 Or Len(lote) = 0 Or Len(cad) = 0 Or Len(CandidatePart(best, 5)) > 0 Then status = "PARTIAL"

    For Each item In ties
        If CandidatePart(CStr(item), 0) <> pc Then pc = "": status = "AMBIGUOUS": explain = "The scan can be interpreted in more than one way. Check the medicine box."
        If CandidatePart(CStr(item), 1) <> sn Then sn = "": status = "AMBIGUOUS": explain = "The scan can be interpreted in more than one way. Check the medicine box."
        If CandidatePart(CStr(item), 2) <> lote Then lote = "": status = "AMBIGUOUS": explain = "The scan can be interpreted in more than one way. Check the medicine box."
        If CandidatePart(CStr(item), 3) <> cad Then cad = "": status = "AMBIGUOUS": explain = "The scan can be interpreted in more than one way. Check the medicine box."
    Next item

    If status = "OK" And Not hasGs And Len(sn) > 0 And Len(sn) < 8 Then
        For Each item In allCandidates
            If CStr(item) <> best And _
               CandidatePart(CStr(item), 0) = CandidatePart(best, 0) And _
               Len(CandidatePart(CStr(item), 5)) = 0 And _
               CountParsedFields(CStr(item)) >= 3 Then
                If CandidatePart(CStr(item), 0) <> pc Then pc = ""
                If CandidatePart(CStr(item), 1) <> sn Then sn = ""
                If CandidatePart(CStr(item), 2) <> lote Then lote = ""
                If CandidatePart(CStr(item), 3) <> cad Then cad = ""
                status = "AMBIGUOUS"
                explain = "The scan can be interpreted in more than one way. Check the medicine box."
            End If
        Next item
    End If

    If status = "PARTIAL" Then explain = BuildPartialExplain(pc, sn, lote, cad, CandidatePart(best, 5))
    If Len(pc) = 0 And Len(sn) = 0 And Len(lote) = 0 And Len(cad) = 0 Then
        status = "UNPARSED"
        explain = "The scan could not be decoded. Check the scanner input or enter the values manually."
    End If

    ResolveTies = CandidateText(pc, sn, lote, cad, CLng(CandidatePart(best, 4)), CandidatePart(best, 5), status, CStr(ConfidenceFor(status, pc, sn, lote, cad, CandidatePart(best, 5))), BoolText(hasGs), explain)
End Function

Private Function CountParsedFields(candidate As String) As Long
    If Len(CandidatePart(candidate, 0)) > 0 Then CountParsedFields = CountParsedFields + 1
    If Len(CandidatePart(candidate, 1)) > 0 Then CountParsedFields = CountParsedFields + 1
    If Len(CandidatePart(candidate, 2)) > 0 Then CountParsedFields = CountParsedFields + 1
    If Len(CandidatePart(candidate, 3)) > 0 Then CountParsedFields = CountParsedFields + 1
End Function

Private Function ScoreCandidate(candidate As String) As Long
    Dim pc As String
    Dim sn As String
    Dim lote As String
    Dim cad As String
    Dim ignored As Long
    Dim leftover As String
    Dim score As Long

    pc = CandidatePart(candidate, 0)
    sn = CandidatePart(candidate, 1)
    lote = CandidatePart(candidate, 2)
    cad = CandidatePart(candidate, 3)
    ignored = CLng(CandidatePart(candidate, 4))
    leftover = CandidatePart(candidate, 5)

    If Len(pc) > 0 And Len(sn) > 0 And Len(lote) > 0 And Len(cad) > 0 Then score = score + 1000000
    If Len(pc) > 0 Then score = score + 100000
    If Len(sn) > 0 Then score = score + 100000
    If Len(lote) > 0 Then score = score + 100000
    If Len(cad) > 0 Then score = score + 100000
    If Len(leftover) = 0 Then score = score + 10000
    score = score + (ignored * 1000)
    If IsValidGtinCheckDigit(pc) Then score = score + 20
    If Len(cad) > 0 Then score = score + 10
    score = score - Len(sn) - Len(lote)
    If StartsWithAny(lote, "10,17,21,71") Then score = score - 30
    If StartsWithAny(sn, "10,17") Then score = score - 10

    ScoreCandidate = score
End Function

Private Function CandidateText(pc As String, sn As String, lote As String, cad As String, ignored As Long, leftover As String, status As String, Optional confidence As String = "", Optional hasGs As String = "", Optional explain As String = "") As String
    CandidateText = pc & vbTab & sn & vbTab & lote & vbTab & cad & vbTab & CStr(ignored) & vbTab & leftover & vbTab & status & vbTab & confidence & vbTab & hasGs & vbTab & explain
End Function

Private Function CandidatePart(candidate As String, index As Long) As String
    Dim parts() As String
    parts = Split(candidate, vbTab)
    If index <= UBound(parts) Then CandidatePart = parts(index) Else CandidatePart = ""
End Function

Private Function WithField(candidate As String, fieldName As String, value As String) As String
    Dim pc As String
    Dim sn As String
    Dim lote As String
    Dim cad As String
    Dim idx As Long

    pc = CandidatePart(candidate, 0)
    sn = CandidatePart(candidate, 1)
    lote = CandidatePart(candidate, 2)
    cad = CandidatePart(candidate, 3)

    Select Case fieldName
        Case "PC": idx = 0
        Case "SN": idx = 1
        Case "LOTE": idx = 2
        Case "CAD": idx = 3
    End Select

    If Len(CandidatePart(candidate, idx)) > 0 Then
        WithField = ""
        Exit Function
    End If

    Select Case fieldName
        Case "PC": pc = value
        Case "SN": sn = value
        Case "LOTE": lote = value
        Case "CAD": cad = value
    End Select

    WithField = CandidateText(pc, sn, lote, cad, CLng(CandidatePart(candidate, 4)), CandidatePart(candidate, 5), CandidatePart(candidate, 6))
End Function

Private Function WithIgnored71(candidate As String) As String
    WithIgnored71 = CandidateText(CandidatePart(candidate, 0), CandidatePart(candidate, 1), CandidatePart(candidate, 2), CandidatePart(candidate, 3), CLng(CandidatePart(candidate, 4)) + 1, CandidatePart(candidate, 5), CandidatePart(candidate, 6))
End Function

Private Function NormalizeGtin(gtin As String) As String
    If Left$(gtin, 1) = "0" Then NormalizeGtin = Mid$(gtin, 2) Else NormalizeGtin = gtin
End Function

Private Function IsDigits(value As String) As Boolean
    Dim i As Long
    If Len(value) = 0 Then Exit Function
    For i = 1 To Len(value)
        If Mid$(value, i, 1) < "0" Or Mid$(value, i, 1) > "9" Then Exit Function
    Next i
    IsDigits = True
End Function

Private Function IsVariableValue(value As String) As Boolean
    Dim i As Long
    Dim ch As String
    Dim code As Long
    If Len(value) = 0 Then Exit Function
    For i = 1 To Len(value)
        ch = Mid$(value, i, 1)
        code = AscW(ch)
        If code < 32 Or code > 126 Then Exit Function
    Next i
    IsVariableValue = True
End Function

Private Function IsValidExpiry(expiry As String) As Boolean
    Dim yy As Long
    Dim mm As Long
    Dim dd As Long
    Dim maxDay As Long

    yy = CLng(Left$(expiry, 2))
    mm = CLng(Mid$(expiry, 3, 2))
    dd = CLng(Right$(expiry, 2))
    If mm < 1 Or mm > 12 Then Exit Function
    If dd = 0 Then IsValidExpiry = True: Exit Function

    Select Case mm
        Case 1, 3, 5, 7, 8, 10, 12: maxDay = 31
        Case 4, 6, 9, 11: maxDay = 30
        Case 2
            If yy Mod 4 = 0 Then maxDay = 29 Else maxDay = 28
    End Select
    IsValidExpiry = (dd <= maxDay)
End Function

Private Function IsValidGtinCheckDigit(pc As String) As Boolean
    Dim gtin As String
    Dim i As Long
    Dim digit As Long
    Dim total As Long
    Dim factor As Long
    Dim expected As Long

    gtin = pc
    If Len(gtin) = 13 Then gtin = "0" & gtin
    If Len(gtin) <> 14 Or Not IsDigits(gtin) Then Exit Function

    factor = 3
    For i = Len(gtin) - 1 To 1 Step -1
        digit = CLng(Mid$(gtin, i, 1))
        total = total + digit * factor
        If factor = 3 Then factor = 1 Else factor = 3
    Next i
    expected = (10 - (total Mod 10)) Mod 10
    IsValidGtinCheckDigit = (expected = CLng(Right$(gtin, 1)))
End Function

Private Function StartsWithAny(value As String, prefixes As String) As Boolean
    Dim parts() As String
    Dim i As Long
    parts = Split(prefixes, ",")
    For i = LBound(parts) To UBound(parts)
        If Left$(value, Len(parts(i))) = parts(i) Then StartsWithAny = True: Exit Function
    Next i
End Function

Private Function BoolText(value As Boolean) As String
    If value Then BoolText = "TRUE" Else BoolText = "FALSE"
End Function

Private Function ConfidenceFor(status As String, pc As String, sn As String, lote As String, cad As String, leftover As String) As Long
    Dim parsed As Long

    If Len(pc) > 0 Then parsed = parsed + 1
    If Len(sn) > 0 Then parsed = parsed + 1
    If Len(lote) > 0 Then parsed = parsed + 1
    If Len(cad) > 0 Then parsed = parsed + 1

    Select Case status
        Case "OK"
            ConfidenceFor = 100
        Case "AMBIGUOUS"
            ConfidenceFor = 45 + parsed * 10
        Case "PARTIAL"
            ConfidenceFor = parsed * 20
            If Len(leftover) > 0 Then ConfidenceFor = ConfidenceFor - 10
            If ConfidenceFor < 20 Then ConfidenceFor = 20
        Case Else
            ConfidenceFor = 0
    End Select
End Function

Private Function BuildPartialExplain(pc As String, sn As String, lote As String, cad As String, leftover As String) As String
    Dim missing As String

    If Len(pc) = 0 Then missing = AppendName(missing, "PC")
    If Len(sn) = 0 Then missing = AppendName(missing, "SN")
    If Len(lote) = 0 Then missing = AppendName(missing, "LOTE")
    If Len(cad) = 0 Then missing = AppendName(missing, "CAD")

    If Len(leftover) > 0 Then
        BuildPartialExplain = "Some fields could not be found. Review this row."
    Else
        BuildPartialExplain = "Some fields could not be found. Review this row."
    End If
End Function

Private Function AppendName(existing As String, name As String) As String
    If Len(existing) = 0 Then
        AppendName = name
    Else
        AppendName = existing & ", " & name
    End If
End Function

Private Sub ApplyDataMatrixFormatting(ws As Worksheet, lastRow As Long)
    Dim rowIndex As Long
    Dim status As String
    Dim rowRange As Range
    Dim statusCell As Range
    Dim fieldCell As Range

    If lastRow < 2 Then Exit Sub

    For rowIndex = 2 To lastRow
        status = UCase$(Trim$(SafeText(ws.Cells(rowIndex, 6).Value)))
        Set rowRange = ws.Range(ws.Cells(rowIndex, 1), ws.Cells(rowIndex, 9))
        Set statusCell = ws.Cells(rowIndex, 6)

        rowRange.Font.Bold = False
        rowRange.Interior.Pattern = xlSolid

        Select Case status
            Case "OK"
                rowRange.Interior.Color = RGB(226, 239, 218)
                rowRange.Font.Color = RGB(55, 86, 35)
                statusCell.Interior.Color = RGB(198, 239, 206)
                statusCell.Font.Color = RGB(0, 97, 0)
            Case "PARTIAL"
                rowRange.Interior.Color = RGB(255, 242, 204)
                rowRange.Font.Color = RGB(126, 96, 0)
                statusCell.Interior.Color = RGB(255, 235, 156)
                statusCell.Font.Color = RGB(156, 101, 0)
            Case "AMBIGUOUS"
                rowRange.Interior.Color = RGB(248, 203, 173)
                rowRange.Font.Color = RGB(132, 60, 12)
                statusCell.Interior.Color = RGB(255, 199, 206)
                statusCell.Font.Color = RGB(156, 0, 6)
                For Each fieldCell In ws.Range(ws.Cells(rowIndex, 2), ws.Cells(rowIndex, 5))
                    If Len(SafeText(fieldCell.Value)) = 0 Then
                        fieldCell.Interior.Color = RGB(244, 176, 132)
                        fieldCell.Font.Color = RGB(156, 0, 6)
                        fieldCell.Font.Bold = True
                    End If
                Next fieldCell
            Case "UNPARSED"
                rowRange.Interior.Color = RGB(217, 217, 217)
                rowRange.Font.Color = RGB(89, 89, 89)
                statusCell.Interior.Color = RGB(191, 191, 191)
                statusCell.Font.Color = RGB(64, 64, 64)
        End Select

        statusCell.Font.Bold = True
        If UCase$(Trim$(SafeText(ws.Cells(rowIndex, 8).Value))) = "TRUE" Then
            ws.Cells(rowIndex, 8).Interior.Color = RGB(221, 235, 247)
            ws.Cells(rowIndex, 8).Font.Color = RGB(31, 78, 121)
            ws.Cells(rowIndex, 8).Font.Bold = True
        End If
    Next rowIndex
End Sub
