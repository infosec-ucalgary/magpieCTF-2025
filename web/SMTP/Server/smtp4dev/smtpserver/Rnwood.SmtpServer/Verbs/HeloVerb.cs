// <copyright file="HeloVerb.cs" company="Rnwood.SmtpServer project contributors">
// Copyright (c) Rnwood.SmtpServer project contributors. All rights reserved.
// Licensed under the BSD license. See LICENSE.md file in the project root for full license information.
// </copyright>

using System.Threading.Tasks;
using Rnwood.SmtpServer.Verbs;

namespace Rnwood.SmtpServer;

/// <summary>
///     Defines the <see cref="HeloVerb" />.
/// </summary>
public class HeloVerb : IVerb
{
    /// <inheritdoc />
    public async Task Process(IConnection connection, SmtpCommand command)
    {
        if (!string.IsNullOrEmpty(connection.Session.ClientName))
        {
            await connection.WriteResponse(new SmtpResponse(
                StandardSmtpResponseCode.BadSequenceOfCommands,
                "You already said HELO, give me a break")).ConfigureAwait(false);
            return;
        }

        connection.Session.ClientName = command.ArgumentsText ?? string.Empty;
        await connection.WriteResponse(new SmtpResponse(StandardSmtpResponseCode.OK, "RoyceWare FLAG Exfiltration Server Welcomes You!"))
            .ConfigureAwait(false);
    }
}
